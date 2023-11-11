from database.db import get_connection
from models.entities.Movie import Movie


class MovieModel:
    @classmethod
    def get_movies(self):
        try:
            connection = get_connection()
            movies = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title, year FROM movie")
                resultset = cursor.fetchall()

                for row in resultset:
                    movie = Movie(row[0], row[1], row[2])
                    movies.append(movie.to_JSON())

            connection.close()
            return movies
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register_movie(cls, title, year):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                # Encuentra el máximo valor de 'id' en la tabla 'movie'
                cursor.execute("SELECT MAX(id) FROM movie")
                max_id = cursor.fetchone()[0]

                if max_id is not None:
                    # Si se encontró un valor máximo, suma uno para obtener el próximo 'id'
                    movie_id = max_id + 1
                else:
                    # Si no se encontró ningún valor, inicia en 1
                    movie_id = 1

                # Verifica si el 'id' ya existe en la tabla 'movie'
                cursor.execute("SELECT COUNT(*) FROM movie WHERE id = %s", (movie_id,))
                count = cursor.fetchone()[0]

                if count == 0:
                    # No existe un registro con el 'id' calculado, procede a la inserción
                    cursor.execute(
                        "INSERT INTO movie (id, title, year) VALUES (%s, %s, %s)",
                        (movie_id, title, year),
                    )
                    connection.commit()
                else:
                    # Ya existe un registro con el 'id' calculado, maneja la situación según tus necesidades
                    print("Ya existe un registro con el ID calculado.")

            connection.close()
            return movie_id
        except Exception as ex:
            raise Exception(ex)
