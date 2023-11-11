from flask import Blueprint, request, jsonify, make_response

# Models
from models.entities.User import User

# Security
from utils.Security import Security

# Services
from models.AuthService import AuthService

main = Blueprint("auth_blueprint", __name__)


@main.route("/", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    _user = User(0, None, None, email, password)
    authenticated_user = AuthService.login_user(_user)

    if authenticated_user != None:
        # Crear una respuesta JSON con el token y los datos del usuario en el cuerpo
        encoded_token = Security.generate_token(authenticated_user)
        user_data = authenticated_user.to_JSON()  # Serializa los datos del usuario
        response_data = {"success": True, "token": encoded_token, "user": user_data}
        response = jsonify(response_data)

        # Establecer el token en el encabezado de la respuesta
        response.headers["Authorization"] = "Bearer " + encoded_token

        return response

    else:
        response = jsonify({"message": "Unauthorized"})
        return response, 401
