from flask import request
from flask_restx import Namespace, Resource, fields
from app.utils.security import hash_password
from app.models.user_model import (
    get_all_users,
    get_user_by_id,
    insert_user,
    update_user,
    delete_user
)

#  Namespace
user_ns = Namespace("users", description="User operations")


# 📦 Request Model (Swagger UI)
user_model = user_ns.model("User", {
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password"),
    "fullname": fields.String(required=True, description="Full Name"),
    "role": fields.String(required=True, description="Role (admin/user)")
})

update_user_model = user_ns.model("UpdateUser", {
    "username": fields.String(required=False),
    "password": fields.String(required=False),
    "fullname": fields.String(required=False),
})

# =========================
# 🔹 GET ALL + INSERT
# =========================
@user_ns.route("/")
class UserList(Resource):

    # ✅ Get all users
    def get(self):
        users = get_all_users()
        return users, 200

    # ✅ Create new user
    @user_ns.expect(user_model)
    def post(self):
        data = request.json

        user = insert_user(data)

        return {
            "message": "User created successfully",
            "user": user
        }, 201


# =========================
# 🔹 GET BY ID / UPDATE / DELETE
# =========================
@user_ns.route("/<string:user_id>")
class User(Resource):

    # ✅ Get user by ID
    def get(self, user_id):
        user = get_user_by_id(user_id)

        if not user:
            return {"message": "User not found"}, 404

        return user, 200

    # ✅ Update user
    @user_ns.expect(update_user_model)

    def put(self, user_id):
        data = request.json or {}
        user = update_user(user_id, data)


        if not data:
            return {"message": "User not found"}, 400

        # 🔐 Prevent updating sensitive fields
        data.pop("role", None)

        # 🔐 Handle password update safely
        if "password" in data:
            from app.utils.security import hash_password
            data["password"] = hash_password(data["password"])

        user = update_user(user_id, data)

        if not user:
            return {"message": "User not found"}, 404

        return {
            "message": "User updated successfully",
            "user": user
        }, 200

    # ✅ Delete user
    def delete(self, user_id):
        success = delete_user(user_id)

        if not success:
            return {"message": "User not found"}, 404

        return {"message": "User deleted successfully"}, 200