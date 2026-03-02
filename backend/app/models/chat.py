from enum import Enum
from typing import List, Optional, Dict, Literal, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RoleEnum(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class Message(BaseModel):
    role: RoleEnum
    content: str
    name: Optional[str] = None
    images: Optional[List[str]] = Field(default=None, description="List of base64 encoded images")
    timestamp: datetime = Field(default_factory=datetime.now)

class ModeEnum(str, Enum):
    WORK = "work"
    EXPERT = "expert"
    LIFE = "life"
    LEARN = "learn"

class IntentEnum(str, Enum):
    QA_KNOWLEDGE = "qa_knowledge"
    TASK_EXECUTION = "task_execution"
    PLANNING = "planning"
    DECISION_SUPPORT = "decision_support"
    SOCIAL_CHAT = "social_chat"
    LEARNING_TUTOR = "learning_tutor"
    MANAGEMENT = "management"
    REFLECTION_EVOLUTION = "reflection_evolution"
    REMINDER = "reminder"
    # Fallback/Legacy
    CHAT = "social_chat"
    QA = "qa_knowledge"
    EXECUTION = "task_execution"

class ChatRequest(BaseModel):
    messages: List[Message]
    stream: bool = True
    session_id: Optional[str] = None
    preferred_model: Optional[str] = None

class RouteInfo(BaseModel):
    primary_mode: ModeEnum = ModeEnum.WORK
    primary_intent: IntentEnum = IntentEnum.SOCIAL_CHAT
    confidence: float = 1.0
    reasoning: Optional[str] = None

class BrainResponseMetadata(BaseModel):
    route: RouteInfo
    processing_time: float
    token_usage: Optional[Dict[str, int]] = None
    sources: List[str] = Field(default_factory=list)
    tool_call: Optional[Dict[str, Any]] = None
    tool_status: Optional[str] = None  # pending, executed, failed

class ChatResponse(BaseModel):
    content: str
    metadata: Optional[BrainResponseMetadata] = None

ProviderName = Literal["gpt5-1", "gemini3", "qwen"]

class ModelRouteResult(BaseModel):
    provider: ProviderName
    endpoint: str
    model_name: str
    model_label: str
    fallback: bool = False
