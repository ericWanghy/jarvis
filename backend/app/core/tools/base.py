from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, action: str, params: Dict[str, Any]) -> Any:
        pass
