# /commands/update_user.py

from src.commands.base_command import BaseCommand
from src.models.model import User
from src.models.schemas import UpdateUserSchema
from src.errors.errors import InvalidParams, UserNotFound
from src.database import db_session

class UpdateUser(BaseCommand):
    def __init__(self, user_id, status=None, dni=None, fullName=None, phoneNumber=None):
        self.user_id = user_id
        self.status = status
        self.dni = dni
        self.fullName = fullName
        self.phoneNumber = phoneNumber

    def execute(self):
        user = db_session.query(User).filter(User.id == self.user_id).first()
        if not user:
            raise UserNotFound()

        data = {
            "status": self.status,
            "dni": self.dni,
            "fullName": self.fullName,
            "phoneNumber": self.phoneNumber
        }

        schema = UpdateUserSchema()
        errors = schema.validate(data)
        if errors:
            raise InvalidParams(errors)

        # Actualizar los campos que no son None
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)

        # Confirmar los cambios en la base de datos
        db_session.commit()

        return {"msg": "el usuario ha sido actualizado"}