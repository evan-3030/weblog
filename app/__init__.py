from flask import Flask
from flask_restx import Api
from app.config import Config
from app.extensions import jwt, create_es
from app.routes.auth import auth_ns
from app.routes.user import user_ns



# ✅ Swagger Authorize (Bearer Token)
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type: Bearer <JWT_TOKEN>"
    }
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)

    app.es = create_es()

    api = Api(
        app,
        title="Weblog API",
        version="1.0",
        description="Auth API with JWT",
        authorizations=authorizations,
        security="Bearer"  
    )

    # ✅ add namespace
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(user_ns, path="/user")

    return app

