from typing import List, Optional
from datetime import datetime
from app.models.chat import Message, RouteInfo, IntentEnum, ModeEnum
from app.core.services.memory import MemoryService
from app.core.services.reminder import ReminderService
from app.core.services.calendar import CalendarService
from app.core.services.prompt import PromptService
from app.core.services.history import HistoryService

class ContextAssembler:
    def __init__(self,
                 memory_service: Optional[MemoryService] = None,
                 reminder_service: Optional[ReminderService] = None,
                 calendar_service: Optional[CalendarService] = None,
                 prompt_service: Optional[PromptService] = None,
                 history_service: Optional[HistoryService] = None):
        self.memory_service = memory_service
        self.reminder_service = reminder_service
        self.calendar_service = calendar_service
        self.prompt_service = prompt_service or PromptService()
        self.history_service = history_service

    def assemble(self, messages: List[Message], route: Optional[RouteInfo] = None, prefetched_data: Optional[dict] = None) -> str:
        """
        Builds the final system prompt based on route and context.
        Using dynamic prompt loading from file system.
        """
        parts = []
        prefetched_data = prefetched_data or {}

        # 1. Determine Base Prompt
        if route is None:
            # SINGLE CALL PATH: Load the generic prompt that includes routing instructions
            system_base = self.prompt_service.get_prompt("system/system_generic.md")
            if not system_base:
                # Fallback to core if generic is missing
                system_base = self.prompt_service.get_prompt("system/system_core.md")
                system_base += "\n\nIMPORTANT: Please determine the user intent and help them."
            parts.append(f"{system_base}\n\nCurrent Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        else:
            # LEGACY/ROUTED PATH: Load core + mode + intent
            system_core = self.prompt_service.get_prompt("system/system_core.md")
            if not system_core:
                system_core = "You are Jarvis, an AI assistant."

            parts.append(f"{system_core}\n\nCurrent Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            # Mode Addon
            mode_file = f"modes/mode_{route.primary_mode.value}.md"
            mode_prompt = self.prompt_service.get_prompt(mode_file)
            if mode_prompt:
                parts.append(f"\n\n--- MODE: {route.primary_mode.value.upper()} ---\n{mode_prompt}")

            # Intent Instruction
            intent_file = f"intents/intent_{route.primary_intent.value}.md"
            intent_prompt = self.prompt_service.get_prompt(intent_file)
            if intent_prompt:
                parts.append(f"\n\n--- INTENT: {route.primary_intent.value.upper()} ---\n{intent_prompt}")

            # Policy: Next Actions (if WORK or PLANNING)
            if route.primary_mode == ModeEnum.WORK or route.primary_intent == IntentEnum.PLANNING:
                policy_prompt = self.prompt_service.get_prompt("policies/next_actions_policy.md")
                if policy_prompt:
                    parts.append(f"\n\n--- POLICY: NEXT ACTIONS ---\n{policy_prompt}")

        # 4. Dynamic Policies (Common)
        # Policy: Reminder Block (if reminders are pending)
        pending_reminders = prefetched_data.get('reminders', [])
        if not pending_reminders and self.reminder_service and 'reminders' not in prefetched_data:
             pending_reminders = self.reminder_service.get_pending_reminders()

        if pending_reminders:
            policy_prompt = self.prompt_service.get_prompt("policies/reminder_block_policy.md")
            if policy_prompt:
                parts.append(f"\n\n--- POLICY: REMINDER BLOCK ---\n{policy_prompt}")

        # Policy: Tool Action Plan (Always include for safety)
        policy_prompt = self.prompt_service.get_prompt("policies/tool_action_plan_policy.md")
        if policy_prompt:
            parts.append(f"\n\n--- POLICY: ACTION PLAN ---\n{policy_prompt}")

        # 5. Data Injection
        parts.append("\n\n--- CONTEXT INJECTION ---")

        # Calendar
        events = prefetched_data.get('events', [])
        if not events and self.calendar_service and 'events' not in prefetched_data:
            events = self.calendar_service.get_events(days=1)

        if events:
            event_text = "\n".join([f"- {e['summary']} at {e['start_time']}" for e in events])
            parts.append(f"\n## Calendar (Next 24h)\n{event_text}")

        # Reminders
        if pending_reminders:
            reminder_text = "\n".join([f"- [ ] {r.title} (Due: {r.due_date})" for r in pending_reminders])
            parts.append(f"\n## Pending Reminders (Context only: DO NOT list these unless the user explicitly asks about tasks/todos)\n{reminder_text}")

        # Memories
        memories = prefetched_data.get('memories', [])
        if not memories and self.memory_service and 'memories' not in prefetched_data:
            memories = self.memory_service.get_memories(limit=5)

        if memories:
            memory_text = "\n".join([f"- {m.content}" for m in memories])
            parts.append(f"\n## Relevant Memories\n{memory_text}")

        # 6. History (CRITICAL)
        history_text = prefetched_data.get('history', "")
        if not history_text and self.history_service and 'history' not in prefetched_data:
            # We fetch recent turns from DB (excluding current turn which is in `messages`)
            history_text = self.history_service.get_context_string(limit=10)

        if history_text:
            parts.append(f"\n## Recent Conversation History\n{history_text}")

        return "\n".join(parts)
