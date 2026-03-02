from __future__ import annotations

import json
import logging
import uuid
from typing import Any, Dict, Generator, List

import requests
from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMProviderError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class BaseProvider:
    def generate(self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any) -> str:
        raise NotImplementedError

    def generate_stream(
        self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any
    ) -> Generator[str, None, None]:
        raise NotImplementedError


class GPT5Provider(BaseProvider):
    """Internal GPT5-1 provider using HTTP POST."""

    def __init__(self) -> None:
        self.endpoint = f"{settings.LLM_BASE_URL}/chat/completions/{settings.LLM_MODEL}"
        self.headers = {
            "BCS-APIHub-RequestId": "jarvis-gpt5-1",
            "X-CHJ-GWToken": settings.LLM_GATEWAY_TOKEN,
            "Content-Type": "application/json",
        }

    def _detect_mime_type(self, b64_str: str) -> str:
        """Simple heuristic to detect MIME type from base64 string."""
        if b64_str.startswith("/9j/"):
            return "image/jpeg"
        if b64_str.startswith("iVBOR"):
            return "image/png"
        if b64_str.startswith("R0lGOD"):
            return "image/gif"
        if b64_str.startswith("UklGR"):
            return "image/webp"
        return "image/jpeg"  # Default fallback

    def _prepare_payload(self, messages: List[Dict[str, Any]], stream: bool = True, **kwargs: Any) -> Dict[str, Any]:
        formatted_messages = []

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            images = msg.get("images", [])

            if role == "system":
                formatted_messages.append({"role": "system", "content": content})
            else:
                # Handle multimodal content
                if images and len(images) > 0:
                    content_parts: List[Dict[str, Any]] = [{"type": "text", "text": content}]
                    for img_b64 in images:
                        # Ensure base64 string has data URI prefix if missing
                        if "," in img_b64:
                            url = img_b64
                        else:
                            mime_type = self._detect_mime_type(img_b64)
                            url = f"data:{mime_type};base64,{img_b64}"

                        content_parts.append({"type": "image_url", "image_url": {"url": url}})

                    formatted_messages.append({"role": role, "content": content_parts})
                else:
                    # Text only
                    formatted_messages.append({"role": role, "content": content})

        return {
            "messages": formatted_messages,
            "max_tokens": kwargs.get("max_tokens", 60000),
            "temperature": kwargs.get("temperature", 0.5),
            "stream": stream,
        }

    def generate(self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any) -> str:
        # Inject system prompt
        msgs_to_send = list(messages)
        if system_prompt:
            msgs_to_send.insert(0, {"role": "system", "content": system_prompt})

        payload = self._prepare_payload(msgs_to_send, stream=False, **kwargs)

        try:
            resp = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=settings.LLM_TIMEOUT)
            if resp.status_code >= 400:
                raise LLMProviderError("internal llm bad status", resp.status_code)
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as e:
            raise LLMProviderError(f"internal llm network error: {e}") from e
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
            raise LLMProviderError(f"internal llm response format error: {e}") from e

    def generate_stream(
        self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any
    ) -> Generator[str, None, None]:
        # Inject system prompt
        msgs_to_send = list(messages)
        if system_prompt:
            msgs_to_send.insert(0, {"role": "system", "content": system_prompt})

        payload = self._prepare_payload(msgs_to_send, stream=True, **kwargs)

        try:
            response = requests.post(
                self.endpoint, headers=self.headers, json=payload, stream=True, timeout=settings.LLM_TIMEOUT
            )

            if response.status_code >= 400:
                raise LLMProviderError(f"internal llm bad status: {response.status_code}", response.status_code)

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data:"):
                        data_str = line_str[5:].strip()
                        if data_str == "[DONE]":
                            break

                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except requests.RequestException as e:
            raise LLMProviderError(f"internal llm streaming network error: {e}") from e


class Gemini3Provider(BaseProvider):
    """Internal Gemini3 provider; same gateway, different model."""

    def __init__(self) -> None:
        self.endpoint = f"{settings.GEMINI_BASE_URL}/chat/completions/{settings.GEMINI_MODEL}"
        self.gw_token = settings.GEMINI_GW_TOKEN

    def _get_headers(self) -> Dict[str, str]:
        return {
            "BCS-APIHub-RequestId": str(uuid.uuid4()),
            "X-CHJ-GWToken": self.gw_token,
            "Content-Type": "application/json",
        }

    def _detect_mime_type(self, b64_str: str) -> str:
        """Simple heuristic to detect MIME type from base64 string."""
        if b64_str.startswith("/9j/"):
            return "image/jpeg"
        if b64_str.startswith("iVBOR"):
            return "image/png"
        if b64_str.startswith("R0lGOD"):
            return "image/gif"
        if b64_str.startswith("UklGR"):
            return "image/webp"
        return "image/jpeg"  # Default fallback

    def _prepare_payload(self, messages: List[Dict[str, Any]], stream: bool = True, **kwargs: Any) -> Dict[str, Any]:
        formatted_messages = []

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            images = msg.get("images", [])

            if role == "system":
                formatted_messages.append({"role": "system", "content": content})
            else:
                # Handle multimodal content
                if images and len(images) > 0:
                    content_parts: List[Dict[str, Any]] = [{"type": "text", "text": content}]
                    for img_b64 in images:
                        # Ensure base64 string has data URI prefix if missing
                        if "," in img_b64:
                            url = img_b64
                        else:
                            mime_type = self._detect_mime_type(img_b64)
                            url = f"data:{mime_type};base64,{img_b64}"

                        content_parts.append({"type": "image_url", "image_url": {"url": url}})

                    formatted_messages.append({"role": role, "content": content_parts})
                else:
                    # Text only
                    formatted_messages.append({"role": role, "content": content})

        return {
            "messages": formatted_messages,
            "max_tokens": kwargs.get("max_tokens", 60000),
            "temperature": kwargs.get("temperature", 0.5),
            "stream": stream,
        }

    def generate(self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any) -> str:
        # Inject system prompt
        msgs_to_send = list(messages)
        if system_prompt:
            msgs_to_send.insert(0, {"role": "system", "content": system_prompt})

        payload = self._prepare_payload(msgs_to_send, stream=False, **kwargs)
        headers = self._get_headers()

        try:
            resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=settings.LLM_TIMEOUT)
            if resp.status_code >= 400:
                raise LLMProviderError("internal gemini llm bad status", resp.status_code)
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as e:
            raise LLMProviderError(f"internal gemini network error: {e}") from e
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
            raise LLMProviderError(f"internal gemini response format error: {e}") from e

    def generate_stream(
        self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any
    ) -> Generator[str, None, None]:
        # Inject system prompt
        msgs_to_send = list(messages)
        if system_prompt:
            msgs_to_send.insert(0, {"role": "system", "content": system_prompt})

        payload = self._prepare_payload(msgs_to_send, stream=True, **kwargs)
        headers = self._get_headers()

        try:
            response = requests.post(
                self.endpoint, headers=headers, json=payload, stream=True, timeout=settings.LLM_TIMEOUT
            )

            if response.status_code >= 400:
                raise LLMProviderError(f"internal gemini llm bad status: {response.status_code}", response.status_code)

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data:"):
                        data_str = line_str[5:].strip()
                        if data_str == "[DONE]":
                            break

                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except requests.RequestException as e:
            raise LLMProviderError(f"internal gemini streaming network error: {e}") from e


class QwenProvider(BaseProvider):
    """Public Qwen provider via OpenAI-compatible client."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.QWEN_API_KEY, base_url=settings.QWEN_BASE_URL)
        self.model = settings.QWEN_MODEL_NAME

    def generate(self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any) -> str:
        # Inject system prompt as the first message if provided
        final_messages = []
        if system_prompt:
            final_messages.append({"role": "system", "content": system_prompt})

        # Clean messages to remove internal 'images' key and ensure OpenAI compatibility
        for msg in messages:
            final_messages.append({
                "role": msg.get("role"),
                "content": msg.get("content")
            })

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=final_messages,
                stream=False,
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            raise LLMProviderError(f"qwen error: {e}") from e

    def generate_stream(
        self, messages: List[Dict[str, Any]], system_prompt: str | None = None, **kwargs: Any
    ) -> Generator[str, None, None]:
        # Inject system prompt as the first message if provided
        final_messages = []
        if system_prompt:
            final_messages.append({"role": "system", "content": system_prompt})

        # Clean messages to remove internal 'images' key and ensure OpenAI compatibility
        for msg in messages:
            final_messages.append({
                "role": msg.get("role"),
                "content": msg.get("content")
            })

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=final_messages,
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            raise LLMProviderError(f"qwen streaming error: {e}") from e
