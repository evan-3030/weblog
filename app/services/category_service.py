# app/services/category_service.py

from datetime import datetime
from app.models.category_model import CategoryModel
from app.extensions import es   # ✅ IMPORTANT CHANGE

INDEX = "categories"


class CategoryService:
    def __init__(self):
        self.es = es

    # ---------------- CREATE ----------------
    def create_category(self, data: dict):
        category = CategoryModel(**data)

        self.es.index(
            index=INDEX,
            id=category.id,
            document=category.to_dict(),
        )

        return category.to_dict()

    # ---------------- GET ALL ----------------
    def get_all_categories(self):
        res = self.es.search(index=INDEX, query={"match_all": {}})
        categories = [hit["_source"] for hit in res["hits"]["hits"]]

        return self.build_tree(categories)

    # ---------------- UPDATE ----------------
    def update_category(self, category_id: str, data: dict):
        data["updated_at"] = datetime.utcnow().isoformat()

        self.es.update(
            index=INDEX,
            id=category_id,
            doc=data,
        )

        updated = self.es.get(index=INDEX, id=category_id)
        return updated["_source"]

    # ---------------- DELETE ----------------
    def delete_category(self, category_id: str):
        self.es.delete(index=INDEX, id=category_id)
        return {"message": "Category deleted successfully"}

    # ---------------- TREE STRUCTURE ----------------
    def build_tree(self, categories):
        category_map = {c["id"]: {**c, "children": []} for c in categories}
        tree = []

        for cat in category_map.values():
            parent_id = cat.get("parent_id")

            if parent_id and parent_id in category_map:
                category_map[parent_id]["children"].append(cat)
            else:
                tree.append(cat)

        return tree