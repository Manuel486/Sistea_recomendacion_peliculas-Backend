from database.db import get_connection
from .entities.User import User


class UserModel:
    @classmethod
    def get_users(self):
        try:
            connection = get_connection()
            users = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, names, lastnames, email, password FROM user")
                resultset = cursor.fetchall()

                for row in resultset:
                    user = User(row[0], row[1], row[2], row[3], row[4])
                    users.append(user.to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(cls, user):
        try:
            connection = get_connection()

            # Verificar si el correo electrónico ya está en uso
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM user WHERE email = %s", (user.email,)
                )
                email_count = cursor.fetchone()[0]

            if email_count > 0:
                return None  # O puedes lanzar una excepción indicando que el correo ya está en uso

            # Verificar si la contraseña ya está en uso
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM user WHERE password = %s", (user.password,)
                )
                password_count = cursor.fetchone()[0]

            if password_count > 0:
                return None  # O puedes lanzar una excepción indicando que la contraseña ya está en uso

            # Si no hay coincidencias de correo y contraseña, procede a insertar el usuario
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO user (names, lastnames, email, password) 
                                VALUES (%s, %s, %s, %s)""",
                    (user.names, user.lastnames, user.email, user.password),
                )
                connection.commit()

                # Obtén el ID del usuario recién agregado
                user_id = cursor.lastrowid

                # Recupera el usuario completo utilizando el ID
                cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()

                # Crea un objeto User a partir de los datos recuperados
                user = User(
                    user_id,
                    user_data[1],  # names
                    user_data[2],  # lastnames
                    user_data[3],  # email
                    user_data[4],  # password
                )

            connection.close()
            return user
        except Exception as ex:
            raise Exception(ex)
