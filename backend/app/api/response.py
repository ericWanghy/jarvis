from flask import jsonify
from typing import Any, Optional, Tuple

def api_success(data: Any = None, status_code: int = 200) -> Tuple[Any, int]:
    return jsonify({"success": True, "data": data, "error": None}), status_code

def api_error(message: str, status_code: int = 400) -> Tuple[Any, int]:
    return jsonify({"success": False, "data": None, "error": message}), status_code
