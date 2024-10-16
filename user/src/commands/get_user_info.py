# /commands/get_user_info.py
from src.commands.base_command import BaseCommand
from src.models.model import User
from src.errors.errors import InvalidParams, UserNotFound, InvalidToken
from src.commands.generate_token import decode_token
from src.database import db_session
import uuid

class GetUserInfo(BaseCommand):
    def __init__(self, token):
        self.token = token

    def execute(self):
        user_id = decode_token(self.token)
        if not user_id:
            raise InvalidToken()

        user = db_session.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user:
            raise UserNotFound()

        return {
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "fullName": user.fullName,
            "dni": user.dni,
            "phoneNumber": user.phoneNumber,
            "status": user.status.value
        }