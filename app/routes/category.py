# app/resources/category.py

from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.category_service import CategoryService
from flask_jwt_extended import jwt_required



category_ns = Namespace("categories", description="Category Operations")

service = CategoryService()


# ---------------- Swagger Model ----------------
category_model = category_ns.model(
    "Category",
    {
        "id": fields.String(readonly=True),
        "title": fields.String(required=True),
        "description": fields.String,
        "parent_id": fields.String,
    },
)


# ================= CATEGORY LIST =================
@category_ns.route("")
class CategoryList(Resource):

    @category_ns.expect(category_model)
    @jwt_required()
    def post(self):
        """Create category"""
        data = request.json
        return service.create_category(data), 201

    def get(self):
        """Get categories with nested tree"""
        return service.get_all_categories(), 200


# ================= SINGLE CATEGORY =================
@category_ns.route("/<string:category_id>")
class CategoryDetail(Resource):

    @category_ns.expect(category_model)
    @jwt_required()
    def put(self, category_id):
        """Update category"""
        data = request.json
        return service.update_category(category_id, data), 200

    def delete(self, category_id):
        """Delete category"""
        return service.delete_category(category_id), 200