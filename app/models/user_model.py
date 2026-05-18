from flask import current_app
import uuid

INDEX = "users"


def ensure_index():
    if not current_app.es.indices.exists(index=INDEX):
        current_app.es.indices.create(
            index=INDEX,
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "username": {"type": "keyword"},
                        "password": {"type": "text"},
                        "fullname": {"type": "text"}
                    }
                }
            }
        )


def get_user_by_username(username):
    ensure_index()

    res = current_app.es.search(
        index=INDEX,
        body={
            "query": {
                "match": {
                    "username": username
                }
            }
        }
    )

    hits = res.get("hits", {}).get("hits", [])

    if hits:
        return hits[0]["_source"]

    return None




# 1️⃣ Get by ID
def get_user_by_id(user_id):
    ensure_index()

    try:
        res = current_app.es.get(index=INDEX, id=user_id)
        return res["_source"]
    except Exception:
        return None


# 2️⃣ Get all documents
def get_all_users():
    ensure_index()

    res = current_app.es.search(
        index=INDEX,
        body={
            "query": {
                "match_all": {}
            }
        }
    )

    hits = res.get("hits", {}).get("hits", [])

    return [doc["_source"] for doc in hits]


# 3️⃣ Insert document
def insert_user(data):
    ensure_index()

    user_id = str(uuid.uuid4())
    data["id"] = user_id

    current_app.es.index(
        index=INDEX,
        id=user_id,
        document=data
    )

    return data


# 4️⃣ Update document
def update_user(user_id, data):
    ensure_index()

    try:
        current_app.es.update(
            index=INDEX,
            id=user_id,
            body={
                "doc": data
            }
        )
        return get_user_by_id(user_id)
    except Exception:
        return None


# 5️⃣ Delete document
def delete_user(user_id):
    ensure_index()

    try:
        current_app.es.delete(index=INDEX, id=user_id)
        return True
    except Exception:
        return False