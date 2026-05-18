from flask_restx import Namespace, Resource, fields
from app.services.auth_service import register_user, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

auth_ns = Namespace("auth", description="Authentication operations")


# ================== MODELS ==================

user_model = auth_ns.model("User", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
    "fullname": fields.String
})

login_model = auth_ns.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
})

create_index_model = auth_ns.model('CreateIndexModel', {
    'index': fields.String(required=True)
})


# ================== AUTH ROUTES ==================

from flask_restx import Resource
from flask import request
from app.services.auth_service import register_user, login_user


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_user)
    def post(self):
        data = self.api.payload

        user = register_user(data)

        return {
            "message": "User created",
            "user": user
        }, 201


from flask_jwt_extended import create_access_token, create_refresh_token

@auth_ns.route("/login")
class Login(Resource):

    @auth_ns.expect(login_model, validate=True)
    def post(self):
        data = request.json
        result, status = login_user(data)

        # ❌ if login failed
        if status != 200:
            return result, status

        username = data["username"]

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200
    





@auth_ns.route("/register")
class Register(Resource):

    @auth_ns.expect(user_model, validate=True)
    def post(self):
        return register_user(request.json)


@auth_ns.route("/logout")
class Logout(Resource):

    @jwt_required()
    def post(self):
        return {"message": "Logout successful"}, 200
    





    from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

@auth_ns.route("/refresh")
class Refresh(Resource):

    @auth_ns.doc(security="Bearer")   # 🔒 Swagger support
    @jwt_required(refresh=True)       # ✅ ONLY refresh token allowed
    def post(self):
        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity=current_user)

        return {
            "access_token": new_access_token
        }, 200


# ================== ELASTIC ROUTES ==================

from app.extensions import create_es

@auth_ns.route("/create-index")
class CreateIndex(Resource):

    @auth_ns.expect(create_index_model)
    def post(self):
        es = create_es()

        try:
            data = request.get_json()

            if not data or "index" not in data:
                return {"error": "index field is required"}, 400

            index_name = data["index"].strip().lower()

            print("INDEX NAME:", index_name)

            # Validate index name
            if not index_name:
                return {"error": "index_name is empty"}, 400

            if " " in index_name:
                return {"error": "index_name must not contain spaces"}, 400

            # Check if exists
            if es.indices.exists(index=index_name):
                return {"message": "Index already exists"}, 200

            # Create index
            es.indices.create(index=index_name)

            return {
                "message": f"Index '{index_name}' created successfully"
            }, 201

        except Exception as e:
            print("ERROR:", str(e))
            return {"error": str(e)}, 500


@auth_ns.route("/indices")
class ListIndices(Resource):

    def get(self):
        es = create_es()

        try:
            indices = es.cat.indices(format="json")

            result = [
                {
                    "index": item.get("index"),
                    "docs_count": item.get("docs.count"),
                    "health": item.get("health"),
                    "status": item.get("status")
                }
                for item in indices
            ]

            return {"indices": result}, 200

        except Exception as e:
            return {"error": str(e)}, 500