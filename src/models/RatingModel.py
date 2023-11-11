from database.db import get_connection
from models.entities.Rating import Rating


class RatingModel:
    @classmethod
    def get_ratings(self):
        try:
            connection = get_connection()
            raitings = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, movieId, userId, rating FROM rating")
                resultset = cursor.fetchall()

                for row in resultset:
                    raiting = Rating(row[0], row[1], row[2], row[3])
                    raitings.append(raiting.to_JSON())

            connection.close()
            return raitings
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_ratings_by_user(self, id):
        try:
            connection = get_connection()
            raitings = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT movieId, rating FROM rating WHERE userId = %s ORDER BY movieId DESC",
                    (id,),
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    raiting = Rating(None, row[0], None, row[1])
                    raitings.append(raiting.to_JSON_2_variables())

            connection.close()
            return raitings
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register_rating(cls, movieId, userId, rating):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                # Verifica si ya existe una valoración para la combinación movieId y userId
                cursor.execute(
                    "SELECT COUNT(*) FROM rating WHERE movieId = %s AND userId = %s",
                    (movieId, userId),
                )
                count = cursor.fetchone()[0]
                print("El count es : ", count)

                if count == 0:
                    # No existe una valoración, realiza la inserción
                    cursor.execute(
                        "INSERT INTO rating (movieId, userId, rating) VALUES (%s, %s, %s)",
                        (movieId, userId, rating),
                    )
                    affected_rows = cursor.rowcount
                    print("Columnas afectadas insert : ", affected_rows)
                else:
                    # Ya existe una valoración, actualiza el rating
                    cursor.execute(
                        "UPDATE rating SET rating = %s WHERE movieId = %s AND userId = %s",
                        (rating, movieId, userId),
                    )
                    affected_rows = cursor.rowcount
                    print("Columnas afectadas update : ", affected_rows)

                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
