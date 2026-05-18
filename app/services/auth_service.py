from flask import current_app
from app.utils.security import hash_password, verify_password
from flask_jwt_extended import create_access_token
from app.models.user_model import get_user_by_username, insert_user

def register_user(data):
    username = data.get("username")
    password = data.get("password")
    data.pop("role", None)

    # ✅ Set safe default
    data["role"] = "user"

    if not username or not password:
        return {"message": "Username and password required"}, 400

    # check existing user
    existing = get_user_by_username(username)
    if existing:
        return {"message": "User already exists"}, 400

    # hash password
    hashed_password = hash_password(password)

    user = {
        "username": username,
        "password": hashed_password,
        "fullname": data.get("fullname", "")
    }

    insert_user(user)

    return {"message": "User registered successfully"}, 201


def login_user(data):
    username = data.get("username")
    password = data.get("password")

    user = get_user_by_username(username)

    if not user:
        return {"message": "Invalid credentials"}, 401

    if not verify_password(password, user["password"]):
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(identity=username)

    return {
        "message": "Login successful",
        "access_token": access_token
    }, 200