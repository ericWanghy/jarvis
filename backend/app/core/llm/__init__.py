from typing import Generator, List

from app.core.llm_providers import Gemini3Provider
from app.models.chat import Message


class _LegacyLLMAdapter:
    """
    Adapter to maintain backward compatibility with the old LLMClient interface
    while using the new Gemini3Provider.
    """

    def __init__(self) -> None:
        self.provider = Gemini3Provider()

    def chat_complete(self, messages: List[Message], system_prompt: str | None = None) -> str:
        # Convert Message objects to dicts
        msgs_dicts = []
        for m in messages:
            msg_dict = {"role": m.role.value, "content": m.content}
            if m.images:
                msg_dict["images"] = m.images
            msgs_dicts.append(msg_dict)

        return self.provider.generate(msgs_dicts, system_prompt=system_prompt)

    def chat_stream(self, messages: List[Message], system_prompt: str | None = None) -> Generator[str, None, None]:
        # Convert Message objects to dicts
        msgs_dicts = []
        for m in messages:
            msg_dict = {"role": m.role.value, "content": m.content}
            if m.images:
                msg_dict["images"] = m.images
            msgs_dicts.append(msg_dict)

        return self.provider.generate_stream(msgs_dicts, system_prompt=system_prompt)


def get_llm_client() -> _LegacyLLMAdapter:
    return _LegacyLLMAdapter()
