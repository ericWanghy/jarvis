from flask import Blueprint, request
from sqlalchemy import desc
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import logging

from app.core.database import get_db_session
from app.models.sql import SessionModel, MessageModel
from app.api.response import api_success, api_error

sessions_bp = Blueprint("sessions", __name__)

# --- Pydantic Models for Response ---

class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    meta_json: Optional[dict] = None
    created_at: datetime
    session_id: Optional[str] = None

    class Config:
        from_attributes = True

# --- Endpoints ---

@sessions_bp.route("", methods=["POST"])
def create_session():
    """Create a new empty chat session."""
    try:
        with get_db_session() as db:
            session = SessionModel()
            db.add(session)
            db.commit()
            db.refresh(session)
            return api_success(SessionResponse.model_validate(session).model_dump(mode="json"))
    except Exception as e:
        return api_error(str(e), 500)

@sessions_bp.route("", methods=["GET"])
def list_sessions():
    """List all chat sessions, ordered by most recently updated."""
    try:
        with get_db_session() as db:
            # Increased limit to 1000 to show all sessions by default
            limit = request.args.get("limit", default=1000, type=int)
            sessions = db.query(SessionModel).order_by(desc(SessionModel.updated_at)).limit(limit).all()
            return api_success([SessionResponse.model_validate(s).model_dump(mode="json") for s in sessions])
    except Exception as e:
        return api_error(str(e), 500)

@sessions_bp.route("/<session_id>", methods=["GET"])
def get_session_messages(session_id):
    """Get all messages for a specific session."""
    try:
        with get_db_session() as db:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return api_error("Session not found", 404)

            # Return messages sorted by creation time
            messages = db.query(MessageModel).filter(MessageModel.session_id == session_id).order_by(MessageModel.created_at.asc()).all()
            return api_success([MessageResponse.model_validate(m).model_dump(mode="json") for m in messages])
    except Exception as e:
        return api_error(str(e), 500)

@sessions_bp.route("/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    """Delete a session and all its messages."""
    try:
        with get_db_session() as db:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return api_error("Session not found", 404)

            db.delete(session)
            db.commit()
            return api_success(None)
    except Exception as e:
        return api_error(str(e), 500)
