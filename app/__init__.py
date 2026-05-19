<<<<<<< HEAD
=======
from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended import JWTManager
>>>>>>> 95a2f5c (add category evan)
from flask import Flask
from flask_restx import Api
from app.config import Config
from app.extensions import jwt, create_es
from app.routes.auth import auth_ns
<<<<<<< HEAD
from app.routes.user import user_ns
=======
from app.routes.posts import posts_ns
from app.routes.tags import tags_ns
from app.routes.category import category_ns
>>>>>>> 95a2f5c (add category evan)



# ✅ Swagger Authorize (Bearer Token)
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type: Bearer <JWT_TOKEN>"
    }
}


<<<<<<< HEAD
=======
# JWT INIT
# =========================
jwt = JWTManager()



>>>>>>> 95a2f5c (add category evan)
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)

    app.es = create_es()

<<<<<<< HEAD
=======


>>>>>>> 95a2f5c (add category evan)
    api = Api(
        app,
        title="Weblog API",
        version="1.0",
        description="Auth API with JWT",
        authorizations=authorizations,
<<<<<<< HEAD
        security="Bearer"  
    )

    # ✅ add namespace
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(user_ns, path="/user")

    return app

=======
        security="Bearer"
    )

    # ✅ Namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(posts_ns, path="/posts")
    api.add_namespace(tags_ns, path="/tags")
    api.add_namespace(category_ns, path="/categories")



    # =========================
    # jwt ERROR HANDLING
    # =========================

    @app.errorhandler(NoAuthorizationError)
    def handle_missing_auth(error):
        return jsonify({
            "message": "User not found or not logged in"
        }), 404

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return {"message": "User not logged in"}, 401
    

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({
            "message": "User not found or not logged in"
        }), 404

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({
            "message": "Token expired, please login again"
        }), 404

    return app
>>>>>>> 95a2f5c (add category evan)
