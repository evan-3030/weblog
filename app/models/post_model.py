# import uuid
# from datetime import datetime

# class PostModel:

#     @staticmethod
#     def create_post_document(data, author_id):

#         now = datetime.utcnow().isoformat()

# app/models/post_model.py

# Post model dictionary for Elasticsearch storage

import uuid
from datetime import datetime


class PostModel:

    @staticmethod
    def create_post(data, author_id):

        now = datetime.utcnow().isoformat()

        return {
            "id": str(uuid.uuid4()),

            "title": data.get("title"),

            "body": data.get("body"),

            "author": author_id,

            "tags": data.get("tags", []),

            "created_at": now,

            "updated_at": now
        }