# app/models/tag_model.py

# Tag model dictionary for Elasticsearch storage

import uuid
from datetime import datetime


class TagModel:

    @staticmethod
    def create_tag(data):

        now = datetime.utcnow().isoformat()

        return {

            "id": str(uuid.uuid4()),

            "title": data.get("title"),

            "description": data.get("description"),

            "created_at": now,

            "updated_at": now
        }