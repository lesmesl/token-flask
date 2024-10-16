import base64

from src.commands.base_command import BaseCommand
from src.models.model import User
from src.errors.errors import InvalidParams, UserAlreadyExists
from src.database import db_session
import os
import hashlib
from src.models.schemas import CreateUserInputSchema, ResponseJsonUserSchema

class CreateUser(BaseCommand):
    def __init__(self, username, password, email, dni, fullName, phoneNumber):
        self.username = username
        self.password = password
        self.email = email
        self.dni = dni
        self.fullName = fullName
        self.phoneNumber = phoneNumber

    @staticmethod
    def generate_salt():
        return os.urandom(16)

    @staticmethod
    def hash_password(password, salt):
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(salt, str):
            salt = salt.encode('utf-8')
        salted_password = password + salt
        return hashlib.sha256(salted_password).hexdigest()

    def execute(self):
        # Crear una instancia del esquema de entrada
        input_schema = CreateUserInputSchema()

        # Validar los datos de entrada
        input_data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "dni": self.dni,
            "fullName": self.fullName,
            "phoneNumber": self.phoneNumber
        }

        errors = input_schema.validate(input_data)
        if errors:
            raise InvalidParams(errors)

        # Verificar si el usuario ya existe
        existing_user = db_session.query(User).filter(
            (User.username == self.username) | (User.email == self.email)
        ).first()
        if existing_user:
            raise UserAlreadyExists()

        # Generar el salt
        salt = self.generate_salt()

        # Hashear la contraseña con el salt
        hashed_password = self.hash_password(self.password, salt)

        salt_base64 = base64.b64encode(salt).decode('utf-8')

        new_user = User(
            username=self.username,
            password=hashed_password,
            dni=self.dni,
            email=self.email,
            fullName=self.fullName,
            phoneNumber=self.phoneNumber,
            salt=salt_base64
        )
        db_session.add(new_user)
        db_session.commit()

        # Serializar la respuesta usando el esquema de salida
        output_schema = ResponseJsonUserSchema()
        # return {"id": new_user.id, "createdAt": new_user.createdAt}
        
        return output_schema.dump(new_user)