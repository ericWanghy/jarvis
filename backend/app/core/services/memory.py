from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.sql import MemoryModel
from typing import List

class MemoryService:
    def __init__(self, db: Session):
        self.db = db

    def add_memory(self, content: str, category: str = "general") -> MemoryModel:
        memory = MemoryModel(content=content, category=category)
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory

    def get_memories(self, limit: int = 10) -> List[MemoryModel]:
        return self.db.query(MemoryModel).order_by(MemoryModel.created_at.desc()).limit(limit).all()

    def search_memories(self, query: str) -> List[MemoryModel]:
        # Simple SQL LIKE search for MVP
        # In future: Replace with Vector Search
        return self.db.query(MemoryModel).filter(MemoryModel.content.ilike(f"%{query}%")).all()

    def search_memories_any(self, keywords: List[str]) -> List[MemoryModel]:
        """Search for memories containing ANY of the keywords."""
        if not keywords:
            return []

        filters = [MemoryModel.content.ilike(f"%{k}%") for k in keywords]
        return self.db.query(MemoryModel).filter(or_(*filters)).all()

    def update_memory(self, memory_id: int, content: str = None, category: str = None) -> MemoryModel:
        memory = self.db.query(MemoryModel).filter(MemoryModel.id == memory_id).first()
        if not memory:
            return None

        if content is not None:
            memory.content = content
        if category is not None:
            memory.category = category

        self.db.commit()
        self.db.refresh(memory)
        return memory

    def delete_memory(self, memory_id: int) -> bool:
        memory = self.db.query(MemoryModel).filter(MemoryModel.id == memory_id).first()
        if not memory:
            return False

        self.db.delete(memory)
        self.db.commit()
        return True
