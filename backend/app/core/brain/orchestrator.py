import json
import logging
import time
import re
from typing import Generator, List, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat import (
    Message,
    BrainResponseMetadata,
    RouteInfo,
    IntentEnum,
    RoleEnum,
    ModeEnum,
    ModelRouteResult,
    ProviderName
)
from app.models.sql import MessageModel
from app.core.brain.context import ContextAssembler
from app.core.llm_providers import GPT5Provider, Gemini3Provider, QwenProvider, LLMProviderError
from app.core.services.memory import MemoryService
from app.core.services.reminder import ReminderService
from app.core.services.calendar import CalendarService
from app.core.services.history import HistoryService

from app.core.tools.registry import ToolRegistry
from app.core.tools.feishu_tool import FeishuTool

logger = logging.getLogger(__name__)

class BrainOrchestrator:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        # Initialize Services
        self.memory_service = MemoryService(db) if db else None
        self.reminder_service = ReminderService(db) if db else None
        self.calendar_service = CalendarService()
        self.history_service = HistoryService(db) if db else None

        # Initialize Tools
        self.tool_registry = ToolRegistry()
        self.tool_registry.register(FeishuTool())

        self.context_assembler = ContextAssembler(
            memory_service=self.memory_service,
            reminder_service=self.reminder_service,
            calendar_service=self.calendar_service,
            history_service=self.history_service
        )

        # Providers
        self.providers = {
            "gpt5-1": GPT5Provider(),
            "gemini3": Gemini3Provider(),
            "qwen": QwenProvider(),
        }

        # Internal state for model routing
        self._internal_available: bool = True

    def _regex_match(self, content: str) -> RouteInfo | None:
        """Fast path for common patterns."""
        content_lower = content.lower()

        # Reminder patterns
        if re.search(r"(remind me|set a reminder|alarm|timer|提醒|闹钟)", content_lower):
            return RouteInfo(
                primary_mode=ModeEnum.LIFE,
                primary_intent=IntentEnum.REMINDER,
                confidence=1.0,
                reasoning="Regex match: Reminder keyword detected"
            )

        # Calendar patterns
        if re.search(r"(calendar|schedule|appointment|meeting|日程|日历|会议)", content_lower):
             return RouteInfo(
                primary_mode=ModeEnum.LIFE,
                primary_intent=IntentEnum.PLANNING, # Or management?
                confidence=0.9,
                reasoning="Regex match: Calendar keyword detected"
            )

        return None

    def _choose_model(
        self,
        preferred_model: Optional[str],
        has_images: bool,
    ) -> ModelRouteResult:
        pm: ProviderName = (preferred_model or "gpt5-1")  # type: ignore[assignment]

        # 内网不可用，统一走 Qwen（除非用户本来就选 qwen）
        if not self._internal_available and pm != "qwen":
            return ModelRouteResult(
                provider="qwen",
                endpoint=settings.QWEN_BASE_URL,
                model_name=settings.QWEN_MODEL_NAME,
                model_label="Qwen 公网（自动降级）",
                fallback=True,
            )

        # 用户显式选 qwen
        if pm == "qwen":
            return ModelRouteResult(
                provider="qwen",
                endpoint=settings.QWEN_BASE_URL,
                model_name=settings.QWEN_MODEL_NAME,
                model_label="Qwen 公网",
            )

        # 用户显式选 gemini3
        if pm == "gemini3":
            return ModelRouteResult(
                provider="gemini3",
                endpoint=f"{settings.GEMINI_BASE_URL}/chat/completions/{settings.GEMINI_MODEL}",
                model_name=settings.GEMINI_MODEL,
                model_label="内网 Gemini3",
            )

        # 默认 gpt5-1
        if pm == "gpt5-1":
            if has_images:
                return ModelRouteResult(
                    provider="gemini3",
                    endpoint=f"{settings.GEMINI_BASE_URL}/chat/completions/{settings.GEMINI_MODEL}",
                    model_name=settings.GEMINI_MODEL,
                    model_label="内网 Gemini3（自动图像切换）",
                )
            return ModelRouteResult(
                provider="gpt5-1",
                endpoint=f"{settings.LLM_BASE_URL}/chat/completions/{settings.LLM_MODEL}",
                model_name=settings.LLM_MODEL,
                model_label="内网 GPT5-1",
            )

        # 理论兜底（不应到达）
        return ModelRouteResult(
            provider="gpt5-1",
            endpoint=f"{settings.LLM_BASE_URL}/chat/completions/{settings.LLM_MODEL}",
            model_name=settings.LLM_MODEL,
            model_label="内网 GPT5-1",
        )

    def _save_message(self, role: str, content: str, meta: Optional[dict] = None, images: Optional[List[str]] = None):
        if not self.db:
            return
        try:
            msg = MessageModel(role=role, content=content, meta_json=meta, images=images)
            self.db.add(msg)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to save message: {e}")

    def _extract_search_terms(self, query: str) -> List[str]:
        """Extract potential search terms from a query string."""
        terms = []

        # 1. Use the full query first (if short enough)
        if len(query) < 50:
            terms.append(query)

        # 2. Split by common Chinese/English delimiters
        # Remove common Chinese particles/verbs
        # 吗 呢 了 的 是 在 有 和 跟 与 几 什 么
        clean_query = re.sub(r"[吗呢了的是在有和跟与几什么]", " ", query)

        # Split by whitespace (handles English and the spaces we just inserted)
        parts = clean_query.split()

        english_stop_words = {"how", "what", "where", "when", "who", "is", "are", "was", "were", "do", "does", "did", "can", "could", "should", "would", "the", "a", "an", "in", "on", "at", "to", "for", "of", "with", "by"}

        for part in parts:
            if part.lower() in english_stop_words:
                continue

            # Filter out very short terms unless they are Chinese characters
            if len(part) > 1:
                terms.append(part)
            elif len(part) == 1 and ord(part) > 127: # Simple check for non-ASCII (likely Chinese)
                # But single char Chinese search is also risky. "我" -> matches everything.
                # Let's skip single chars for now unless we are desperate.
                pass

        # Deduplicate
        return list(set(terms))

    def _prefetch_context_data(self, query: Optional[str] = None) -> dict:
        """Fetch all context data in parallel with routing."""
        data = {}
        try:
            if self.reminder_service:
                data['reminders'] = self.reminder_service.get_pending_reminders()
            if self.calendar_service:
                data['events'] = self.calendar_service.get_events(days=1)
            if self.memory_service:
                if query:
                    # Use smart search with keyword extraction
                    keywords = self._extract_search_terms(query)
                    if keywords:
                        data['memories'] = self.memory_service.search_memories_any(keywords)
                    else:
                        # Fallback if no keywords extracted
                        data['memories'] = self.memory_service.get_memories(limit=5)
                else:
                    # Fallback to recent memories
                    data['memories'] = self.memory_service.get_memories(limit=5)
            if self.history_service:
                data['history'] = self.history_service.get_context_string(limit=100)
        except Exception as e:
            logger.error(f"Context prefetch error: {e}")
        return data

    def _handle_tool_confirmation(self, session_id: str, messages: List[Message]) -> Optional[str]:
        """
        Check if the user is confirming a pending tool call.
        If so, execute it and return the result string.
        """
        if not session_id or not self.db or not messages:
            return None

        last_user_msg = messages[-1]
        if last_user_msg.role != RoleEnum.USER:
            return None

        # Simple confirmation check
        content_lower = last_user_msg.content.lower().strip()
        confirmation_keywords = ["confirm", "proceed", "yes", "do it", "execute", "ok", "go ahead", "确认", "执行", "好的", "没问题"]

        if len(content_lower) < 20 and any(k in content_lower for k in confirmation_keywords):
            # Find the last assistant message in this session
            last_assistant_msg = self.db.query(MessageModel).filter(
                MessageModel.session_id == session_id,
                MessageModel.role == RoleEnum.ASSISTANT
            ).order_by(MessageModel.created_at.desc()).first()

            if last_assistant_msg and last_assistant_msg.meta_json:
                meta = last_assistant_msg.meta_json
                if meta.get("tool_status") == "pending" and meta.get("tool_call"):
                    tool_call = meta["tool_call"]
                    tool_name = tool_call.get("tool")
                    action = tool_call.get("action")
                    params = tool_call.get("params", {})

                    tool = self.tool_registry.get_tool(tool_name)
                    if tool:
                        logger.info(f"Executing confirmed tool: {tool_name}.{action}")
                        try:
                            result = tool.execute(action, params)
                            # Update status to executed
                            meta["tool_status"] = "executed"
                            # SQLAlchemy JSON mutation tracking can be tricky, re-assigning helps
                            last_assistant_msg.meta_json = dict(meta)
                            self.db.commit()
                            return f"Tool Executed Successfully.\nResult: {json.dumps(result, ensure_ascii=False, indent=2)}"
                        except Exception as e:
                            logger.error(f"Tool execution failed: {e}")
                            return f"Tool Execution Failed: {str(e)}"
        return None

    def process_stream(self, messages: List[Message], preferred_model: str | None = None, session_id: str | None = None) -> Generator[str, None, None]:
        start_time = time.time()

        # 0. Check for Tool Confirmation
        tool_result = self._handle_tool_confirmation(session_id, messages)
        if tool_result:
            logger.info("Tool executed based on confirmation. Injecting result into context.")
            # Inject tool result as a SYSTEM message for the LLM to summarize
            messages.append(Message(role=RoleEnum.SYSTEM, content=f"Tool Execution Result: {tool_result}"))

        # 1. Context Prefetch (Parallelized with Regex Check if desired)
        # Optimization: We can still use Router's regex check for super-fast routing
        last_user_content = messages[-1].content if messages else None
        fast_route = self._regex_match(last_user_content) if last_user_content else None
        prefetched_data = self._prefetch_context_data(query=last_user_content)

        # 2. Assemble Context
        # If regex matched, we use the specific route. If not, we pass None to use Generic Prompt.
        system_prompt = self.context_assembler.assemble(
            messages,
            route=fast_route,
            prefetched_data=prefetched_data
        )
        logger.info(f"System Prompt assembled. Length: {len(system_prompt)}")
        if len(system_prompt) < 100:
            logger.warning(f"System prompt too short! Content: {system_prompt}")
        else:
            logger.debug(f"System Prompt Preview: {system_prompt[:100]}...")

        # 3. Decide model route based on preferred_model and images
        has_images = any(m.images for m in messages) if messages else False
        route_choice = self._choose_model(preferred_model, has_images)

        # 4. Stream LLM Response & Parse Intent
        full_content = ""
        buffer = ""
        intent_found = False
        detected_route = fast_route # Start with fast_route if available
        detected_tool_call = None

        # Default fallback route
        default_route = RouteInfo(
            primary_mode=ModeEnum.LIFE,
            primary_intent=IntentEnum.SOCIAL_CHAT,
            confidence=0.0,
            reasoning="Fallback: No intent detected"
        )

        # 调用路由后的 provider；当前保留原有 chat_stream 结构，先整体拿到内容再按原逻辑解析 INTENT
        try:
            provider = self.providers[route_choice.provider]

            # Prepare messages with images
            msgs_dicts = []
            for m in messages:
                msg_dict = {"role": m.role.value, "content": m.content}
                if m.images:
                    msg_dict["images"] = m.images
                msgs_dicts.append(msg_dict)

            chunks = provider.generate_stream(msgs_dicts, system_prompt=system_prompt)

            # Mark success if internal
            if route_choice.provider in ("gpt5-1", "gemini3"):
                self._internal_available = True

            is_fallback = route_choice.fallback
        except LLMProviderError as e:
            logger.error(f"Provider {route_choice.provider} error: {e}")
            is_fallback = False
            # 内网失败则降级到 qwen
            if route_choice.provider in ("gpt5-1", "gemini3"):
                self._internal_available = False
                fallback_route = self._choose_model("qwen", False)
                try:
                    provider = self.providers[fallback_route.provider]
                    chunks = provider.generate_stream(msgs_dicts, system_prompt=system_prompt)

                    is_fallback = True or fallback_route.fallback
                    route_choice = fallback_route
                except LLMProviderError as e2:
                    logger.error(f"Fallback Qwen error: {e2}")
                    raise
            else:
                raise

        for chunk in chunks:
            # If we already have a route (regex) or found the intent, just stream
            if intent_found or fast_route:
                full_content += chunk
                yield chunk
                continue

            # Otherwise, buffer to find <INTENT>
            buffer += chunk

            # Check for closing tag
            if "</INTENT>" in buffer:
                try:
                    # Split buffer: [Intent Block] [Remaining Content]
                    intent_block_raw, remaining_content = buffer.split("</INTENT>", 1)

                    # Extract and Parse JSON
                    json_str = intent_block_raw.split("<INTENT>")[-1].strip()
                    # Handle markdown code blocks if present
                    if "```" in json_str:
                        match = re.search(r"\{.*\}", json_str, re.DOTALL)
                        if match: json_str = match.group(0)

                    data = json.loads(json_str)
                    detected_route = RouteInfo(**data)
                    logger.info(f"Stream-Detected Intent: {detected_route.primary_mode} / {detected_route.primary_intent}")

                    intent_found = True

                    # Yield the remaining content (the actual response)
                    if remaining_content:
                        full_content += remaining_content
                        yield remaining_content

                except Exception as e:
                    logger.error(f"Intent parsing failed: {e}")
                    # Failed to parse, treat buffer as content
                    intent_found = True
                    full_content += buffer
                    yield buffer

            # Check for TOOL_CALL
            elif "</TOOL_CALL>" in buffer:
                try:
                    tool_block_raw, remaining_content = buffer.split("</TOOL_CALL>", 1)
                    json_str = tool_block_raw.split("<TOOL_CALL>")[-1].strip()
                    if "```" in json_str:
                        match = re.search(r"\{.*\}", json_str, re.DOTALL)
                        if match: json_str = match.group(0)

                    detected_tool_call = json.loads(json_str)
                    logger.info(f"Stream-Detected Tool Call: {detected_tool_call}")

                    intent_found = True # Stop buffering

                    if remaining_content:
                        full_content += remaining_content
                        yield remaining_content

                except Exception as e:
                    logger.error(f"Tool call parsing failed: {e}")
                    intent_found = True
                    full_content += buffer
                    yield buffer

            # Safety: If buffer gets too large (e.g. 1000 chars) without tag, assume no intent
            elif len(buffer) > 1000:
                logger.warning("Buffer overflow, assuming no intent tag")
                intent_found = True
                full_content += buffer
                yield buffer

        # Flush buffer if stream ended without intent tag
        if not intent_found and buffer:
            logger.info("Stream ended without intent tag, yielding buffer")
            full_content += buffer
            yield buffer

        # 4. Post-Process & Side Effects
        final_route = detected_route if detected_route else default_route

        # Handle Reminders (Post-Generation)
        # Since we didn't know it was a reminder beforehand, we run extraction now.
        # The LLM has likely already said "I'll set that reminder".
        if final_route.primary_intent == IntentEnum.REMINDER and self.reminder_service:
             if messages and messages[-1].role == RoleEnum.USER:
                try:
                    reminder = self.reminder_service.extract_and_create_reminder(messages[-1].content)
                    if reminder:
                        logger.info(f"Created reminder: {reminder.title}")
                        # We don't inject a system message into the stream (it's too late),
                        # but we save it to DB so it appears in history/logs.
                        self._save_message("system", f"ACTION: Created reminder '{reminder.title}'")
                except Exception as e:
                    logger.error(f"Reminder extraction failed: {e}")

        # Save Assistant Metadata (content DB write is handled in API layer)
        duration = time.time() - start_time
        metadata = BrainResponseMetadata(
            route=final_route,
            processing_time=duration,
            sources=["SingleCallOrchestrator"],
            tool_call=detected_tool_call,
            tool_status="pending" if detected_tool_call else None
        )
        base_meta = metadata.model_dump()
        base_meta["model_provider"] = route_choice.provider
        base_meta["model_label"] = route_choice.model_label
        base_meta["fallback"] = is_fallback

        # Yield hidden metadata for frontend
        yield f"\n__META_JSON__{json.dumps(base_meta, ensure_ascii=False)}"
