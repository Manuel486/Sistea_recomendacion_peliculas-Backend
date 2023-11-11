from flask import Blueprint, jsonify, request

# Entities
from models.entities.User import User

# Models
from models.UserModel import UserModel

main = Blueprint("user_blueprint", __name__)


@main.route("/")
def get_users():
    try:
        users = UserModel.get_users()
        return jsonify(users)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@main.route("/add", methods=["POST"])
def add_user():
    try:
        names = request.json["names"]
        lastnames = request.json["lastnames"]
        email = request.json["email"]
        password = request.json["password"]
        user = User(None, names, lastnames, email, password)

        new_user = UserModel.add_user(user)
        if new_user is not None:
            return jsonify(
                {
                    "id": new_user.id,
                    "names": new_user.names,
                    "lastnames": new_user.lastnames,
                    "email": new_user.email,
                    "password": new_user.password,
                }
            )  # Devuelve el nuevo usuario en formato JSON
        else:
            return jsonify({"message": "Error on insert"}), 500

    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
