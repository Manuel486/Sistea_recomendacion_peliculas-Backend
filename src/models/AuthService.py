# Database
from database.db import get_connection

# Errors
from utils.errors.CustomException import CustomException

# Models
from models.entities.User import User


class AuthService:
    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute(
                    "call sp_verifyIdentity(%s, %s)", (user.email, user.password)
                )
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = User(
                        int(row[0]), row[1], row[2], row[3], row[4]
                    )
            connection.close()
            return authenticated_user
        except CustomException as ex:
            raise CustomException(ex)
