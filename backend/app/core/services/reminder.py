import subprocess
import json
import logging
import platform
from sqlalchemy.orm import Session
from app.models.sql import ReminderModel
from datetime import datetime, timedelta
from typing import List, Optional
from dateutil import rrule, parser
from app.core.llm import get_llm_client
from app.core.services.prompt import PromptService
from app.models.chat import Message, RoleEnum

logger = logging.getLogger(__name__)

class ReminderService:
    def __init__(self, db: Session):
        self.db = db
        self.llm = get_llm_client()
        self.prompt_service = PromptService()

    def add_reminder(self, title: str, due_date: Optional[datetime] = None, recurrence_rule: Optional[str] = None) -> ReminderModel:
        reminder = ReminderModel(
            title=title,
            due_date=due_date,
            recurrence_rule=recurrence_rule
        )
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        logger.info(f"Added reminder: {title} at {due_date}")
        return reminder

    def extract_and_create_reminder(self, user_input: str) -> ReminderModel:
        """
        Extract reminder details from natural language and create it.
        """
        extract_prompt = self.prompt_service.get_prompt("intents/intent_reminder_extract.md")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        system_prompt = extract_prompt.replace("{{current_time}}", current_time).replace("{{input}}", user_input)

        try:
            msgs = [Message(role=RoleEnum.USER, content="Extract reminder info.")]
            response = self.llm.chat_complete(msgs, system_prompt=system_prompt)

            clean_text = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)

            content = data.get("content")
            if not content:
                raise ValueError("Could not extract content")

            due_date_str = data.get("due_date")
            due_date = parser.parse(due_date_str) if due_date_str else None

            recurrence_rule = data.get("recurrence_rule")

            logger.info(f"Extracted reminder: {content}, Due: {due_date}")
            return self.add_reminder(content, due_date, recurrence_rule)

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            # Fallback: just create a simple reminder with the text
            return self.add_reminder(user_input)

    def get_pending_reminders(self) -> List[ReminderModel]:
        # Using 'is_(False)' for SQLAlchemy compliance
        return self.db.query(ReminderModel).filter(ReminderModel.is_completed.is_(False)).order_by(ReminderModel.due_date.asc()).all()

    def get_overdue_reminders(self) -> List[ReminderModel]:
        now = datetime.now()
        return self.db.query(ReminderModel).filter(
            ReminderModel.is_completed.is_(False),
            ReminderModel.due_date < now
        ).order_by(ReminderModel.due_date.asc()).all()

    def get_today_reminders(self) -> List[ReminderModel]:
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        return self.db.query(ReminderModel).filter(
            ReminderModel.is_completed.is_(False),
            ReminderModel.due_date >= start_of_day,
            ReminderModel.due_date <= end_of_day
        ).order_by(ReminderModel.due_date.asc()).all()

    def get_all_reminders(self, limit: int = 200) -> List[ReminderModel]:
        """
        Get all reminders (both pending and completed), sorted by due_date descending.
        """
        return self.db.query(ReminderModel).order_by(ReminderModel.due_date.desc()).limit(limit).all()

    def update_reminder(self, reminder_id: int, **kwargs) -> Optional[ReminderModel]:
        reminder = self.db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
        if not reminder:
            return None

        for key, value in kwargs.items():
            if hasattr(reminder, key):
                setattr(reminder, key, value)

        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def delete_reminder(self, reminder_id: int) -> bool:
        reminder = self.db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
        if not reminder:
            return False

        self.db.delete(reminder)
        self.db.commit()
        return True

    def check_due_reminders(self):
        """
        Check for reminders that are due and haven't been completed.
        Notify if due_date <= now AND (never notified OR notified > 5 mins ago).
        """
        now = datetime.now()
        logger.info(f"Checking due reminders at {now}")

        # Get all pending reminders that are due
        pending = self.db.query(ReminderModel).filter(
            ReminderModel.is_completed.is_(False),
            ReminderModel.due_date <= now
        ).all()

        logger.info(f"Found {len(pending)} pending due reminders")

        for r in pending:
            # Check if we should notify
            should_notify = False
            if not r.last_notified_at:
                should_notify = True
            else:
                # Re-notify every 5 minutes if still pending
                if now - r.last_notified_at > timedelta(minutes=5):
                    should_notify = True

            if should_notify:
                logger.info(f"Sending notification for: {r.title}")
                self.send_system_notification("Reminder Due", r.title)
                r.last_notified_at = now
                self.db.commit()


    def complete_reminder(self, reminder_id: int):
        reminder = self.db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
        if not reminder:
            return

        # Mark current as completed
        reminder.is_completed = True

        # Handle recurrence
        if reminder.recurrence_rule and reminder.due_date:
            try:
                # Calculate next occurrence
                # We use dateutil.rrule to parse the string
                # Note: rrule string from LLM might lack DTSTART, so we might need to prepend it or use the due_date as start
                # A standard RRULE string is like "FREQ=WEEKLY;..."
                # rrule.rrulestr needs a start date to calculate 'after' correctly if DTSTART is missing in rule

                # Construct a full RRULE set
                rule_str = reminder.recurrence_rule
                if "DTSTART" not in rule_str:
                     # This is a bit tricky with rrulestr if strictly following iCal.
                     # Easier way: create rrule object manually or try-catch.
                     # Let's assume standard "FREQ=..." string
                     rule = rrule.rrulestr(rule_str, dtstart=reminder.due_date)
                else:
                     rule = rrule.rrulestr(rule_str)

                next_date = rule.after(reminder.due_date)

                if next_date:
                    # Create the next instance
                    new_reminder = ReminderModel(
                        title=reminder.title,
                        due_date=next_date,
                        recurrence_rule=reminder.recurrence_rule,
                        is_completed=False
                    )
                    self.db.add(new_reminder)
                    logger.info(f"Created next recurring reminder for {next_date}")
                else:
                    logger.info("Recurrence finished (no next date found).")

            except Exception as e:
                logger.error(f"Failed to process recurrence: {e}")

        self.db.commit()

    def send_system_notification(self, title: str, message: str):
        """
        Send macOS native notification using AppleScript.
        On non-macOS platforms, logs the notification instead.
        """
        if platform.system() != "Darwin":
            logger.info("Notification (non-macOS): [%s] %s", title, message)
            return

        try:
            # Escape double quotes to prevent applescript errors
            safe_message = message.replace('"', '\\"')
            safe_title = title.replace('"', '\\"')
            script = f'display notification "{safe_message}" with title "{safe_title}" sound name "default"'
            subprocess.run(["osascript", "-e", script])
        except Exception as e:
            logger.error("Failed to send notification: %s", e)
