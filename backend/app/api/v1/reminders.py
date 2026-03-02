from flask import Blueprint, request
from app.core.database import get_db_session
from app.core.services.reminder import ReminderService
from dateutil import parser
from app.api.response import api_success, api_error

reminders_bp = Blueprint("reminders", __name__)

@reminders_bp.route("/today", methods=["GET"])
def get_today_reminders():
    try:
        with get_db_session() as db:
            service = ReminderService(db)
            reminders = service.get_today_reminders()
            return api_success([{
                "id": r.id,
                "title": r.title,
                "due_date": r.due_date.isoformat() if r.due_date else None,
                "recurrence_rule": r.recurrence_rule,
                "is_completed": r.is_completed
            } for r in reminders])
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("/pending", methods=["GET"])
def get_pending_reminders():
    try:
        with get_db_session() as db:
            service = ReminderService(db)
            reminders = service.get_pending_reminders()
            return api_success([{
                "id": r.id,
                "title": r.title,
                "due_date": r.due_date.isoformat() if r.due_date else None,
                "recurrence_rule": r.recurrence_rule,
                "is_completed": r.is_completed
            } for r in reminders])
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("/overdue", methods=["GET"])
def get_overdue_reminders():
    try:
        with get_db_session() as db:
            service = ReminderService(db)
            reminders = service.get_overdue_reminders()
            return api_success([{
                "id": r.id,
                "title": r.title,
                "due_date": r.due_date.isoformat() if r.due_date else None,
                "recurrence_rule": r.recurrence_rule,
                "is_completed": r.is_completed
            } for r in reminders])
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("/all", methods=["GET"])
def get_all_reminders():
    try:
        with get_db_session() as db:
            service = ReminderService(db)
            limit = request.args.get("limit", 200, type=int)
            reminders = service.get_all_reminders(limit=limit)
            return api_success([{
                "id": r.id,
                "title": r.title,
                "due_date": r.due_date.isoformat() if r.due_date else None,
                "recurrence_rule": r.recurrence_rule,
                "is_completed": r.is_completed
            } for r in reminders])
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("/<int:reminder_id>", methods=["PUT"])
def update_reminder(reminder_id):
    try:
        with get_db_session() as db:
            data = request.json
            service = ReminderService(db)

            due_date = None
            if "due_date" in data:
                if data["due_date"]:
                    try:
                        due_date = parser.parse(data["due_date"])
                    except:
                        pass
                # If due_date is explicitly null in payload, we set it to None.
                # But update_reminder uses kwargs.

            update_data = {}
            if "title" in data: update_data["title"] = data["title"]
            if "recurrence_rule" in data: update_data["recurrence_rule"] = data["recurrence_rule"]
            if "is_completed" in data: update_data["is_completed"] = data["is_completed"]
            if "due_date" in data: update_data["due_date"] = due_date

            reminder = service.update_reminder(reminder_id, **update_data)
            if not reminder:
                return api_error("Reminder not found", 404)

            return api_success({
                "id": reminder.id,
                "title": reminder.title,
                "due_date": reminder.due_date.isoformat() if reminder.due_date else None,
                "recurrence_rule": reminder.recurrence_rule,
                "is_completed": reminder.is_completed
            })
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("/<int:reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    try:
        with get_db_session() as db:
            service = ReminderService(db)
            success = service.delete_reminder(reminder_id)
            if not success:
                return api_error("Reminder not found", 404)
            return api_success({"status": "deleted"})
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("", methods=["POST"])
def create_reminder():
    try:
        with get_db_session() as db:
            data = request.json
            service = ReminderService(db)

            due_date = None
            if data.get("due_date"):
                try:
                    due_date = parser.parse(data.get("due_date"))
                except:
                    pass

            reminder = service.add_reminder(
                title=data.get("title"),
                due_date=due_date,
                recurrence_rule=data.get("recurrence_rule")
            )
            return api_success({
                "id": reminder.id,
                "title": reminder.title,
                "due_date": reminder.due_date.isoformat() if reminder.due_date else None,
                "recurrence_rule": reminder.recurrence_rule,
                "is_completed": reminder.is_completed
            }, 201)
    except Exception as e:
        return api_error(str(e), 500)

@reminders_bp.route("/<int:reminder_id>/complete", methods=["POST"])
def complete_reminder(reminder_id):
    try:
        with get_db_session() as db:
            service = ReminderService(db)
            service.complete_reminder(reminder_id)
            return api_success({"status": "completed"})
    except Exception as e:
        return api_error(str(e), 500)
