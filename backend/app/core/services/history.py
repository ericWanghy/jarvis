from sqlalchemy.orm import Session
from app.models.sql import MessageModel
from typing import List, Dict

class HistoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_recent_turns(self, limit: int = 20) -> List[Dict[str, str]]:
        """
        Fetch recent conversation turns for context injection.
        Returns a list of dicts: [{'role': 'user', 'content': '...', 'created_at': '...'}, ...]
        """
        # Fetch last N messages (descending)
        messages = self.db.query(MessageModel).order_by(MessageModel.created_at.desc()).limit(limit).all()

        # Reverse to chronological order (oldest first)
        messages.reverse()

        return [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.strftime("%Y-%m-%d %H:%M") if m.created_at else "Unknown"
            }
            for m in messages
        ]

    def get_context_string(self, limit: int = 20) -> str:
        """
        Get formatted conversation history string with timestamps.
        """
        turns = self.get_recent_turns(limit)
        if not turns:
            return ""

        lines = []
        for turn in turns:
            role_label = "User" if turn['role'] == 'user' else "Jarvis"
            lines.append(f"[{turn['created_at']}] {role_label}: {turn['content']}")

        return "\n".join(lines)
