import logging
import os
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

class PromptService:
    def __init__(self, prompts_dir: str = "app/prompts"):
        """Prompt loader for markdown templates.

        By default we resolve prompts relative to the backend root so that
        starting the backend from different working directories (e.g. via
        start_dev.sh or directly under backend/) still finds app/prompts.
        """
        from app.core.config import settings

        # Prefer BASE_DIR from settings (backend root), fall back to cwd for safety
        base = getattr(settings, "BASE_DIR", None)
        if base is None:
            base = Path(os.getcwd())
        self.base_dir = base / prompts_dir
        self._cache: Dict[str, str] = {}
        logger.info(f"Base prompts dir: {self.base_dir}")

    def get_prompt(self, relative_path: str, use_cache: bool = True) -> str:
        """
        Reads a markdown prompt file.
        Example path: 'modes/mode_work.md'
        """
        if use_cache and relative_path in self._cache:
            return self._cache[relative_path]

        full_path = self.base_dir / relative_path
        if not full_path.exists():
            logger.warning(f"Prompt file not found: {full_path}")
            return ""

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                self._cache[relative_path] = content
                logger.debug(f"Loaded prompt: {relative_path} ({len(content)} chars)")
                return content
        except Exception as e:
            logger.error(f"Error reading prompt {relative_path}: {e}")
            return ""

    def update_prompt(self, relative_path: str, content: str):
        """
        Updates a prompt file. Invalidates cache.
        """
        full_path = self.base_dir / relative_path
        # Ensure directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        self._cache[relative_path] = content

    def create_prompt(self, relative_path: str, content: str = ""):
        """
        Creates a new prompt file.
        """
        full_path = self.base_dir / relative_path
        if full_path.exists():
            raise FileExistsError(f"Prompt file already exists: {relative_path}")

        # Ensure directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        self._cache[relative_path] = content

    def delete_prompt(self, relative_path: str):
        """
        Deletes a prompt file.
        """
        full_path = self.base_dir / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {relative_path}")

        os.remove(full_path)

        if relative_path in self._cache:
            del self._cache[relative_path]

    def list_prompts(self) -> Dict[str, list]:
        """
        Returns a tree structure of available prompts.
        """
        result = {}
        for root, _, files in os.walk(self.base_dir):
            rel_dir = os.path.relpath(root, self.base_dir)
            if rel_dir == ".":
                continue

            prompt_files = [f for f in files if f.endswith(".md")]
            if prompt_files:
                result[rel_dir] = prompt_files
        return result
