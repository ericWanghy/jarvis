from pydantic_settings import BaseSettings
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    APP_NAME: str = "Jarvis v5.6-proxy"
    ENV: str = "development"
    HOST: str = "127.0.0.1"
    PORT: int = 3721

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "storage"

    # Database
    DATABASE_URL: str = ""

    # LLM Gateway Configuration
    LLM_BASE_URL: str = "http://api-hub.inner.chj.cloud/llm-gateway/v1"
    LLM_MODEL: str = "azure-gpt-5_1"
    LLM_TIMEOUT: int = 60

    # Gemini Configuration
    GEMINI_BASE_URL: str = "http://api-hub.inner.chj.cloud/llm-gateway/v1"
    GEMINI_MODEL: str = "gemini-3-pro-preview"
    ROUTER_MODEL: str = "gemini-3-flash"

    # Qwen Configuration
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    QWEN_MODEL_NAME: str = "qwen3-omni-flash-2025-12-01"

    # Secrets - MUST be set via .env or environment variables
    LLM_GATEWAY_TOKEN: str = ""
    GEMINI_GW_TOKEN: str = ""
    QWEN_API_KEY: str = ""

    # Feishu Configuration
    FEISHU_APP_ID: str = ""
    FEISHU_APP_SECRET: str = ""
    FEISHU_ENCRYPT_KEY: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def _create_settings() -> Settings:
    s = Settings()

    # Resolve DATABASE_URL if not explicitly set
    if not s.DATABASE_URL:
        s.DATABASE_URL = f"sqlite:///{s.DATA_DIR}/jarvis.db"

    # Warn about missing secrets
    missing = []
    if not s.LLM_GATEWAY_TOKEN:
        missing.append("LLM_GATEWAY_TOKEN")
    if not s.GEMINI_GW_TOKEN:
        missing.append("GEMINI_GW_TOKEN")
    if not s.QWEN_API_KEY:
        missing.append("QWEN_API_KEY")

    # Feishu warnings (optional but recommended)
    if not s.FEISHU_APP_ID or not s.FEISHU_APP_SECRET:
        logger.warning("Feishu credentials missing. Feishu integration will not work.")

    if missing:
        logger.warning(
            "Missing required secrets: %s. "
            "Set them in .env or environment variables. See .env.example.",
            ", ".join(missing),
        )

    return s


settings = _create_settings()
os.makedirs(settings.DATA_DIR, exist_ok=True)
