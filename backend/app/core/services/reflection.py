import json
import logging
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.llm import get_llm_client
from app.core.services.prompt import PromptService
from app.models.chat import Message, RoleEnum
from app.models.sql import ReminderModel

logger = logging.getLogger(__name__)

class RuleMatcher:
    def __init__(self, db: Session):
        self.db = db

    def match(self, messages: List[Message]) -> Optional[Dict[str, Any]]:
        """
        Evaluates rules against the conversation history.
        Returns attribution dict if a rule matches, else None.
        """
        if not messages:
            return None

        last_user_msg = next((m for m in reversed(messages) if m.role == RoleEnum.USER), None)
        last_assistant_msg = next((m for m in reversed(messages) if m.role == RoleEnum.ASSISTANT), None)

        # Rule 1: Missing Reminders
        # Trigger: Overdue reminders exist AND assistant didn't mention them
        try:
            overdue_reminders = self.db.query(ReminderModel).filter(
                ReminderModel.due_date < datetime.now(),
                ReminderModel.is_completed == False
            ).count()

            if overdue_reminders > 0 and last_assistant_msg:
                if "【提醒】" not in last_assistant_msg.content and "[Reminder]" not in last_assistant_msg.content:
                    return {
                        "rule_id": "rule_1_missing_reminders",
                        "stage": "reminder_policy",
                        "prompt_targets": ["policies/reminder_block_policy.md", "system/system_core.md"],
                        "confidence": 1.0
                    }
        except Exception as e:
            logger.error(f"Rule 1 check failed: {e}")

        # Rule 2: Output Too Long / User Request Brevity
        LENGTH_THRESHOLD = 2000  # Example threshold
        brevity_keywords = ["太长", "啰嗦", "简短", "只要结论", "too long", "be brief"]

        is_too_long = last_assistant_msg and len(last_assistant_msg.content) > LENGTH_THRESHOLD
        user_asked_brevity = last_user_msg and any(k in last_user_msg.content.lower() for k in brevity_keywords)

        if is_too_long or user_asked_brevity:
            return {
                "rule_id": "rule_2_brevity",
                "stage": "response_format",
                "prompt_targets": ["system/system_core.md"],
                "confidence": 1.0
            }

        # Rule 6: Missing Action Plan
        # Trigger: Assistant says "I have created/sent" but no [ActionPlan] or tool call
        action_claims = ["已经创建", "已经发送", "created", "sent", "updated"]
        has_claim = last_assistant_msg and any(c in last_assistant_msg.content for c in action_claims)
        has_action_plan = last_assistant_msg and ("[ActionPlan]" in last_assistant_msg.content or "tool_calls" in str(last_assistant_msg.meta_json))

        if has_claim and not has_action_plan:
             return {
                "rule_id": "rule_6_missing_action_plan",
                "stage": "tool_or_skill",
                "prompt_targets": ["policies/tool_action_plan_policy.md", "system/system_core.md"],
                "confidence": 1.0
            }

        return None

class ReflectionService:
    def __init__(self, db: Optional[Session] = None):
        self.llm = get_llm_client()
        self.prompt_service = PromptService()
        self.db = db

    def validate_diff(self, target_file: str, diff_content: str) -> bool:
        """
        Validates if the diff can be applied to the target file.
        """
        # Placeholder for diff validation logic
        # In a real implementation, we would use 'patch' or similar library
        return True

    def analyze_recent_turns(self, recent_messages: List[Message]) -> Dict[str, Any]:
        """
        Run the reflection loop on recent messages.
        """
        # 1. Try Deterministic Rules
        if self.db:
            matcher = RuleMatcher(self.db)
            rule_result = matcher.match(recent_messages)
            if rule_result:
                return self._generate_proposal_from_rule(recent_messages, rule_result)

        # 2. Fallback to LLM (existing logic)
        return self._analyze_with_llm(recent_messages)

    def _generate_proposal_from_rule(self, messages: List[Message], rule_result: Dict) -> Dict:
        target = rule_result["prompt_targets"][0]
        current_content = self.prompt_service.get_prompt(target)

        system_prompt = f"""
You are the Evolution Engine. A deterministic rule has identified an issue.
Rule Triggered: {rule_result['rule_id']}
Target File: {target}

Current Content of {target}:
```markdown
{current_content}
```

Generate a Unified Diff to fix this issue based on the conversation history.
Output JSON: {{ "proposals": [ {{ "target": "{target}", "diff": "...", "reasoning": "..." }} ] }}
"""
        conversation_text = "\n".join([f"{m.role}: {m.content}" for m in messages])
        messages_payload = [
            Message(role=RoleEnum.USER, content=f"Here is the conversation log:\n\n{conversation_text}")
        ]

        try:
            response_text = self.llm.chat_complete(messages_payload, system_prompt=system_prompt)
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            logger.error(f"Rule-based Proposal Generation Failed: {e}")
            return {"error": str(e)}

    def _analyze_with_llm(self, recent_messages: List[Message]) -> Dict[str, Any]:
        # Load the reflection intent prompt
        reflection_prompt = self.prompt_service.get_prompt("intents/intent_reflection_evolution.md")
        attribution_rules = self.prompt_service.get_prompt("policies/reflection_attribution_rules.md")

        # Construct the analysis prompt
        system_prompt = f"""
You are the Evolution Engine. Your goal is to improve the system prompts based on user feedback.

{reflection_prompt}

{attribution_rules}

Analyze the following conversation logs and output the JSON.
"""
        conversation_text = "\n".join([f"{m.role}: {m.content}" for m in recent_messages])

        messages = [
            Message(role=RoleEnum.USER, content=f"Here is the conversation log:\n\n{conversation_text}")
        ]

        try:
            response_text = self.llm.chat_complete(messages, system_prompt=system_prompt)
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)

        except Exception as e:
            logger.error(f"Reflection Analysis Failed: {e}")
            return {
                "signals": [],
                "attributions": [],
                "proposals": [],
                "error": str(e)
            }
