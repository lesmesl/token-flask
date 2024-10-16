# /blueprints/user.py
from flask import Blueprint, request, jsonify
from src.commands.create_user import CreateUser
from src.commands.update_user import UpdateUser
from src.commands.generate_token import GenerateToken
from src.commands.get_user_info import GetUserInfo
from src.commands.reset_database import ResetDatabase
from src.errors.errors import InvalidParams, UserAlreadyExists, UserNotFound, InvalidToken, InvalidToken, UserPasswordError,TokenExpired, MissingTokenError
import uuid

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users', methods=['POST'])
def create_user():

    try:
        data = request.get_json()

        create_user_command = CreateUser(
            data.get('username'),
            data.get('password'),
            data.get('email'),
            data.get('dni'),
            data.get('fullName'),
            data.get('phoneNumber')
        ).execute()
        return jsonify(create_user_command), 201
    except InvalidParams:
        return '', 400
    except UserAlreadyExists:
        return '', 412
    except Exception as e:
        return str(e), 400

@user_blueprint.route('/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    try:
        data = request.get_json()

        user_id = uuid.UUID(user_id)  # Asegúrate de que user_id es un UUID válido


        result = UpdateUser(
            user_id,
            data.get('status'),
            data.get('dni'),
            data.get('fullName'),
            data.get('phoneNumber')
        ).execute()
        return jsonify(result), 200
    except InvalidParams:
        return '', 400
    except UserNotFound:
        return '', 404
    except Exception as e:
        return str(e), 400

@user_blueprint.route('/users/auth', methods=['POST'])
def generate_token():
    data = request.get_json()
    try:
        result = GenerateToken(
            data.get('username'),
            data.get('password')
        ).execute()
        return jsonify(result), 200
    except InvalidParams as e:
        return e.description , e.code
    except UserNotFound as e:
        return e.description , e.code
    except UserPasswordError as e:
        return e.description , e.code

@user_blueprint.route('/users/me', methods=['GET'])
def get_user_info():
    auth_header = request.headers.get('Authorization')
    if auth_header and " " in auth_header:
        token = auth_header.split(" ")[1]
        try:
            user_info = GetUserInfo(token).execute()
            return jsonify(user_info), 200
        except (UserNotFound, TokenExpired, InvalidToken, InvalidToken) as e:
            return e.description , e.code
        except Exception as e:
            return str(e), 500
    else:
        return MissingTokenError.description, MissingTokenError.code

@user_blueprint.route('/users/ping', methods=['GET'])
def ping():
    return 'pong', 200

@user_blueprint.route('/users/reset', methods=['POST'])
def reset_database():
    result = ResetDatabase().execute()
    return jsonify(result), 200