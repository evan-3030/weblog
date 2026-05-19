# app/models/category_model.py

from datetime import datetime
from uuid import uuid4


class CategoryModel:
    def __init__(
        self,
        title: str,
        description: str = "",
        parent_id: str = None,
        id: str = None,
        created_at: str = None,
        updated_at: str = None,
    ):
        self.id = id or str(uuid4())
        self.title = title
        self.description = description
        self.parent_id = parent_id
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict):
        return CategoryModel(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )