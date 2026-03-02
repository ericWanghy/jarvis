import json
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
from app.core.llm import get_llm_client
from app.core.services.prompt import PromptService
from app.core.services.memory import MemoryService
from app.models.sql import MessageModel, MemoryModel, SystemStateModel
from app.models.chat import Message, RoleEnum

class MemoryAgent:
    def __init__(self, db: Session):
        self.db = db
        self.llm = get_llm_client()
        self.prompt_service = PromptService()
        self.memory_service = MemoryService(db)

    def scan_new_messages(self) -> List[Dict[str, Any]]:
        """
        Scan NEW messages in batches to extract memories.
        Uses SystemStateModel to track progress (incremental scanning).
        Ensure all extracted memories are in Chinese.
        """
        # 1. Get last scanned message ID
        state = self.db.query(SystemStateModel).filter(SystemStateModel.key == "last_memory_scan_id").first()
        last_scanned_id = int(state.value) if state and state.value else 0

        # 2. Fetch new messages
        new_messages = self.db.query(MessageModel).filter(MessageModel.id > last_scanned_id).order_by(MessageModel.id.asc()).all()

        if not new_messages:
            return []

        # Batch processing configuration
        BATCH_SIZE = 50
        added_memories = []

        # Process in batches
        for i in range(0, len(new_messages), BATCH_SIZE):
            batch = new_messages[i:i + BATCH_SIZE]
            logger.info(f"Scanning batch {i//BATCH_SIZE + 1}/{(len(new_messages)-1)//BATCH_SIZE + 1} ({len(batch)} messages)...")

            # Construct prompt
            scan_prompt = self.prompt_service.get_prompt("intents/intent_memory_scan.md")
            conversation_text = "\n".join([f"{m.role}: {m.content}" for m in batch])

            system_prompt = f"""
{scan_prompt}

IMPORTANT INSTRUCTION:
1. You are scanning a conversation history to extract long-term memories.
2. The 'content' field in your JSON output MUST be written in SIMPLIFIED CHINESE (简体中文), even if the conversation is in English.
3. Translate any English facts/preferences into Chinese for storage.

Analyze the following conversation batch:
{conversation_text}
"""
            try:
                # Call LLM
                msgs = [Message(role=RoleEnum.USER, content="Start scan.")]
                response = self.llm.chat_complete(msgs, system_prompt=system_prompt)

                # Parse JSON
                clean_text = response.replace("```json", "").replace("```", "").strip()
                if not clean_text:
                    # Update checkpoint even if empty, so we don't re-scan empty stuff forever?
                    # Yes, we scanned it.
                    self._update_checkpoint(batch[-1].id)
                    continue

                try:
                    extracted_memories = json.loads(clean_text)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON for batch {i}: {clean_text[:100]}...")
                    # If parsing fails, we MIGHT want to skip updating checkpoint to retry?
                    # But LLM failure might persist. Let's assume we skip this batch for memory but mark as scanned to avoid stuck loop.
                    self._update_checkpoint(batch[-1].id)
                    continue

                if not isinstance(extracted_memories, list):
                    self._update_checkpoint(batch[-1].id)
                    continue

                # Save to DB
                for mem in extracted_memories:
                    if 'content' not in mem or 'category' not in mem:
                        continue

                    # Basic dedup check (exact string match)
                    exists = self.db.query(MemoryModel).filter(MemoryModel.content == mem['content']).first()
                    if not exists:
                        new_mem = self.memory_service.add_memory(mem['content'], mem['category'])
                        added_memories.append({"id": new_mem.id, "content": new_mem.content, "category": new_mem.category})

                # Update checkpoint after successful processing
                self._update_checkpoint(batch[-1].id)

            except Exception as e:
                logger.error(f"Memory Scan Failed for batch {i}: {e}")
                continue

        return added_memories

    def _update_checkpoint(self, last_id: int):
        state = self.db.query(SystemStateModel).filter(SystemStateModel.key == "last_memory_scan_id").first()
        if not state:
            state = SystemStateModel(key="last_memory_scan_id", value=str(last_id))
            self.db.add(state)
        else:
            state.value = str(last_id)
        self.db.commit()

    def consolidate_memories(self) -> Dict[str, Any]:
        """
        Consolidate existing memories.
        """
        # Fetch all memories
        all_memories = self.memory_service.get_memories(limit=100) # Limit for token safety
        if not all_memories:
            return {"status": "no memories to consolidate"}

        memories_json = json.dumps([
            {"id": m.id, "content": m.content, "category": m.category}
            for m in all_memories
        ], indent=2, ensure_ascii=False)

        # Construct prompt
        consolidate_prompt = self.prompt_service.get_prompt("intents/intent_memory_consolidate.md")
        system_prompt = f"""
{consolidate_prompt}

IMPORTANT: All 'content' fields in the output plan MUST be in SIMPLIFIED CHINESE.

Current Memories:
{memories_json}
"""
        try:
            msgs = [Message(role=RoleEnum.USER, content="Start consolidation.")]
            response = self.llm.chat_complete(msgs, system_prompt=system_prompt)

            clean_text = response.replace("```json", "").replace("```", "").strip()
            plan = json.loads(clean_text)

            # Execute Plan
            # 1. Delete
            for mem_id in plan.get("to_delete", []):
                self.db.query(MemoryModel).filter(MemoryModel.id == mem_id).delete()

            # 2. Add
            for mem in plan.get("to_add", []):
                self.memory_service.add_memory(mem['content'], mem['category'])

            # 3. Update
            for mem in plan.get("to_update", []):
                db_mem = self.db.query(MemoryModel).filter(MemoryModel.id == mem['id']).first()
                if db_mem:
                    db_mem.content = mem['content']

            self.db.commit()
            return plan

        except Exception as e:
            logger.error(f"Consolidation Failed: {e}")
            return {"error": str(e)}
