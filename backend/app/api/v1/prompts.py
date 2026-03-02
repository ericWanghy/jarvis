from flask import Blueprint, request
from app.core.services.prompt import PromptService
from app.api.response import api_success, api_error

prompts_bp = Blueprint("prompts", __name__)
prompt_service = PromptService()

@prompts_bp.route("", methods=["GET"])
def list_prompts():
    """List all prompt files in a tree structure"""
    try:
        return api_success(prompt_service.list_prompts())
    except Exception as e:
        return api_error(str(e), 500)

@prompts_bp.route("/content", methods=["GET"])
def get_prompt_content():
    """Get content of a specific prompt file"""
    try:
        path = request.args.get("path")
        if not path:
            return api_error("path is required", 400)

        content = prompt_service.get_prompt(path, use_cache=False)
        return api_success({"content": content})
    except Exception as e:
        return api_error(str(e), 500)

@prompts_bp.route("/content", methods=["POST"])
def update_prompt_content():
    """Update content of a specific prompt file"""
    try:
        data = request.json
        path = data.get("path")
        content = data.get("content")

        if not path or content is None:
            return api_error("path and content are required", 400)

        prompt_service.update_prompt(path, content)
        return api_success({"success": True})
    except Exception as e:
        return api_error(str(e), 500)

@prompts_bp.route("/create", methods=["POST"])
def create_prompt():
    """Create a new prompt file"""
    try:
        data = request.json
        path = data.get("path")
        content = data.get("content", "")

        if not path:
            return api_error("path is required", 400)

        prompt_service.create_prompt(path, content)
        return api_success({"success": True})
    except FileExistsError as e:
        return api_error(str(e), 409)
    except Exception as e:
        return api_error(str(e), 500)

@prompts_bp.route("/delete", methods=["DELETE"])
def delete_prompt():
    """Delete a prompt file"""
    try:
        path = request.args.get("path")
        if not path:
            return api_error("path is required", 400)

        prompt_service.delete_prompt(path)
        return api_success({"success": True})
    except FileNotFoundError as e:
        return api_error(str(e), 404)
    except Exception as e:
        return api_error(str(e), 500)
