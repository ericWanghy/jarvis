import os
import sys
import logging
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.core.tools.registry import ToolRegistry
from app.core.tools.feishu_tool import FeishuTool
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_feishu_tool():
    print("Testing Feishu Tool...")

    # Check config
    if not settings.FEISHU_APP_ID or not settings.FEISHU_APP_SECRET:
        print("Skipping test: Feishu credentials not set in .env")
        return

    registry = ToolRegistry()
    registry.register(FeishuTool())

    tool = registry.get_tool("feishu")
    if not tool:
        print("Error: Feishu tool not found in registry")
        return

    print("Feishu tool registered successfully.")

    # Test a simple read operation (if we had a URL, but we don't want to fail on auth if creds are dummy)
    # So we just check if we can instantiate and call it.

    # We can try to list chats or something simple if we had a valid token.
    # But for now, just verifying the structure is enough.

    print("Test complete.")

if __name__ == "__main__":
    test_feishu_tool()
