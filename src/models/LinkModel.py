from database.db import get_connection
from models.entities.Link import Link


class LinkModel:
    @classmethod
    def get_links(self):
        try:
            connection = get_connection()
            links = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, movieId, imdbId, tmdbId FROM link")
                resultset = cursor.fetchall()

                for row in resultset:
                    link = Link(row[0], row[1], row[2], row[3])
                    links.append(link.to_JSON())

            connection.close()
            return links
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register_link(cls, movieId, imdbId, tmdbId):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO link (movieId, imdbId, tmdbId) VALUES (%s, %s, %s)",
                    (movieId, imdbId, tmdbId),
                )
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
