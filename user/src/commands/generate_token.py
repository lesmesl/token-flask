# /commands/generate_token.py
import base64
import os

from src.commands.base_command import BaseCommand
from src.models.model import User
from src.errors.errors import InvalidParams, UserNotFound, UserPasswordError, TokenExpired, JwtErrorUnknown, InvalidToken
from src.database import db_session
from jose import jwt
from datetime import datetime, timedelta, timezone
import hashlib

SECRET_KEY = "your_secret_key"

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except jwt.JWTError:
        raise InvalidToken()
    except Exception as e:
        raise JwtErrorUnknown(e)


class GenerateToken(BaseCommand):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def hash_password(password, salt):
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(salt, str):
            stored_salt_base64 = salt.encode('utf-8')
            salt = base64.b64decode(stored_salt_base64)
        salted_password = password + salt
        return hashlib.sha256(salted_password).hexdigest()

    def execute(self):
        if not self.username or not self.password:
            raise InvalidParams()

        user = db_session.query(User).filter(User.username == self.username).first()
        if not user:
            raise UserNotFound()

        hashed_password = self.hash_password(self.password, user.salt)

        if hashed_password != user.password:
            raise UserPasswordError()

        expire_at = datetime.now(timezone.utc) + timedelta(hours=1)
        token = jwt.encode({"user_id": str(user.id), "exp": expire_at}, SECRET_KEY, algorithm="HS256")
        expire_at = expire_at.isoformat()

        return {"id": user.id, "token": token, "expireAt": expire_at}