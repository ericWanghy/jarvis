from typing import Any, Dict
from .base import BaseTool
from app.core.skills.feishu.feishu_all_operations import feishu_operation
import logging

logger = logging.getLogger(__name__)

class FeishuTool(BaseTool):
    name = "feishu"
    description = "Feishu (Lark) operations: docs, sheets, bitable, calendar, messages."

    def execute(self, action: str, params: Dict[str, Any]) -> Any:
        """
        Execute a Feishu operation.

        Args:
            action: The specific action to perform (e.g., 'read', 'create', 'send').
            params: Dictionary containing 'type' (doc/sheet/bitable/chat/calendar) and other parameters.
        """
        payload = params.copy()
        payload['action'] = action

        # Ensure 'type' is present
        if 'type' not in payload:
            return {"code": -1, "msg": "Missing 'type' parameter (doc, sheet, bitable, chat, calendar, drive, card)"}

        logger.info(f"Executing Feishu Tool: {payload}")
        try:
            result = feishu_operation(payload)
            return result
        except Exception as e:
            logger.error(f"Feishu Tool Error: {e}", exc_info=True)
            return {"code": -1, "msg": str(e)}
