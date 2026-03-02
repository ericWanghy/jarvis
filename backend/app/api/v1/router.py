import logging
import json
import traceback
from datetime import datetime

from flask import Blueprint, request, Response, stream_with_context
from app.models.chat import ChatRequest
from app.core.brain.orchestrator import BrainOrchestrator
from app.core.database import SessionLocal
from app.models.sql import SessionModel, MessageModel
from app.api.response import api_success, api_error

logger = logging.getLogger(__name__)

api_blueprint = Blueprint("api_v1", __name__)

@api_blueprint.route("/chat", methods=["POST"])
def chat():
    logger.debug(f"Received chat request: {request.json}")

    # The chat endpoint uses a generator for SSE streaming, so the DB session
    # must stay open throughout the generator's lifetime. We keep the manual
    # pattern here but add proper rollback on exceptions.
    db = SessionLocal()

    try:
        data = request.json
        # Validate with Pydantic
        chat_request = ChatRequest(**data)
        preferred_model = chat_request.preferred_model

        has_images = any(m.images for m in chat_request.messages) if chat_request.messages else False

        # Ensure session exists or create one if not provided (though frontend should provide it)
        session_id = chat_request.session_id
        if session_id:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                # If invalid session_id provided, create a new one? Or error?
                # Let's create a new one for robustness
                logger.info(f"Session {session_id} not found, creating new one")
                session = SessionModel(id=session_id, title="New Chat")
                db.add(session)
                db.commit()
            else:
                # Update timestamp
                session.updated_at = datetime.utcnow()
                db.commit()

        # Save USER message to DB
        if chat_request.messages:
            last_user_msg = chat_request.messages[-1]
            if last_user_msg.role == "user":
                db_msg = MessageModel(
                    role="user",
                    content=last_user_msg.content,
                    session_id=session_id
                )
                db.add(db_msg)

                # Auto-name session if it is still the default
                if session_id and session.title == "New Chat":
                    new_title = last_user_msg.content[:50]
                    if len(last_user_msg.content) > 50:
                        new_title += "..."
                    session.title = new_title

                db.commit()

        # Initialize Orchestrator with DB session
        orchestrator = BrainOrchestrator(db=db)

        # Generator for SSE (Server-Sent Events)
        def generate():
            logger.info("Starting stream generation...")
            full_response = ""
            metadata = None

            try:
                for chunk in orchestrator.process_stream(chat_request.messages, preferred_model=preferred_model, session_id=session_id):
                    # Capture full response for saving to DB later
                    full_response += chunk

                    # Check if this chunk contains the metadata trailer
                    if "__META_JSON__" in full_response:
                        parts = full_response.split("__META_JSON__")
                        content_part = parts[0]
                        # We only want to save the content part, but we need to wait until end to be sure
                        try:
                            if len(parts) > 1:
                                metadata = json.loads(parts[1])
                        except:
                            pass

                    yield chunk

                # Stream finished - Save ASSISTANT message to DB
                # Remove the meta trailer from content if present
                content_to_save = full_response
                if "__META_JSON__" in full_response:
                    content_to_save = full_response.split("__META_JSON__")[0]

                # Re-open DB session for saving (generator might run after request context?)
                # Actually we can use the 'db' from outer scope if we are careful about thread safety
                # But stream_with_context runs in request context.

                # We need a new transaction for the save
                try:
                    assistant_msg = MessageModel(
                        role="assistant",
                        content=content_to_save,
                        meta_json=metadata,
                        session_id=session_id
                    )
                    db.add(assistant_msg)
                    db.commit()
                    logger.info(f"Saved assistant response to session {session_id}")
                except Exception as db_e:
                    logger.error(f"Error saving assistant message: {db_e}")
                    db.rollback()

            except Exception as inner_e:
                logger.error(f"Stream Error: {inner_e}", exc_info=True)
                db.rollback()
                yield f"Error in stream: {str(inner_e)}"
            finally:
                # Ensure DB session is closed when stream ends
                db.close()

        return Response(stream_with_context(generate()), mimetype='text/plain')

    except Exception as e:
        logger.error(f"API Error: {e}", exc_info=True)
        db.rollback()
        db.close()
        return api_error(str(e), 500)
