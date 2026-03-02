import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import get_db_session
from app.core.services.reminder import ReminderService
from app.core.services.memory_agent import MemoryAgent

logger = logging.getLogger(__name__)

def job_check_reminders():
    """
    Background job to check for due reminders.
    Creates a new DB session for thread safety.
    """
    with get_db_session() as db:
        try:
            service = ReminderService(db)
            service.check_due_reminders()
        except Exception as e:
            logger.error(f"Scheduler Error: {e}")

def job_daily_memory_scan():
    """
    Daily job (6:00 AM) to:
    1. Incrementally scan new messages for memories.
    2. Consolidate and refine memories.
    """
    with get_db_session() as db:
        try:
            agent = MemoryAgent(db)
            logger.info("Starting Daily Memory Scan (Incremental)...")
            agent.scan_new_messages()
            logger.info("Starting Daily Memory Consolidation...")
            agent.consolidate_memories()
            logger.info("Daily Memory Tasks Completed.")
        except Exception as e:
            logger.error(f"Memory Scheduler Error: {e}")

def init_scheduler():
    scheduler = BackgroundScheduler()
    # Check reminders every 60s
    scheduler.add_job(func=job_check_reminders, trigger="interval", seconds=60)

    # Run memory scan & consolidation daily at 6:00 AM
    scheduler.add_job(func=job_daily_memory_scan, trigger="cron", hour=6, minute=0)

    scheduler.start()
    logger.info("Background Scheduler Started.")

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
