from flask import Blueprint, request
from app.core.database import get_db_session
from app.core.services.memory import MemoryService
from app.core.services.memory_agent import MemoryAgent
from app.api.response import api_success, api_error

memories_bp = Blueprint("memories", __name__)

@memories_bp.route("", methods=["GET"])
def list_memories():
    try:
        with get_db_session() as db:
            service = MemoryService(db)
            memories = service.get_memories(limit=100)
            return api_success([{
                "id": m.id,
                "content": m.content,
                "category": m.category,
                "created_at": m.created_at
            } for m in memories])
    except Exception as e:
        return api_error(str(e), 500)

@memories_bp.route("", methods=["POST"])
def create_memory():
    try:
        with get_db_session() as db:
            data = request.json
            service = MemoryService(db)
            memory = service.add_memory(data.get("content"), data.get("category", "general"))
            return api_success({
                "id": memory.id,
                "content": memory.content,
                "category": memory.category,
                "created_at": memory.created_at
            }, 201)
    except Exception as e:
        return api_error(str(e), 500)

@memories_bp.route("/<int:memory_id>", methods=["PUT"])
def update_memory(memory_id):
    try:
        with get_db_session() as db:
            data = request.json
            service = MemoryService(db)
            memory = service.update_memory(memory_id, data.get("content"), data.get("category"))
            if not memory:
                return api_error("Memory not found", 404)

            return api_success({
                "id": memory.id,
                "content": memory.content,
                "category": memory.category,
                "created_at": memory.created_at,
                "updated_at": memory.updated_at
            })
    except Exception as e:
        return api_error(str(e), 500)

@memories_bp.route("/<int:memory_id>", methods=["DELETE"])
def delete_memory(memory_id):
    try:
        with get_db_session() as db:
            service = MemoryService(db)
            success = service.delete_memory(memory_id)
            if not success:
                return api_error("Memory not found", 404)
            return api_success({"status": "deleted"})
    except Exception as e:
        return api_error(str(e), 500)

@memories_bp.route("/scan", methods=["POST"])
def scan_memories():
    """Trigger incremental scan"""
    try:
        with get_db_session() as db:
            agent = MemoryAgent(db)
            added = agent.scan_new_messages()
            return api_success({"added": added, "count": len(added)})
    except Exception as e:
        return api_error(str(e), 500)

@memories_bp.route("/consolidate", methods=["POST"])
def consolidate_memories():
    """Trigger deep consolidation"""
    try:
        with get_db_session() as db:
            agent = MemoryAgent(db)
            result = agent.consolidate_memories()
            return api_success(result)
    except Exception as e:
        return api_error(str(e), 500)
