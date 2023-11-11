from flask import Blueprint, jsonify, request
from models.LinkModel import LinkModel

import pandas as pd
from models.MovieModel import MovieModel

# Entities
from models.entities.Rating import Rating

# Models
from models.RatingModel import RatingModel
from utils.Security import Security

main = Blueprint("rating_blueprint", __name__)


@main.route("/")
def get_ratings():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            ratings = RatingModel.get_ratings()
            return jsonify(ratings)
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500
    else:
        response = jsonify({"message": "Unauthorized"})
        return response, 401


@main.route("/<id>")
def get_ratings_by_user(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            ratings = RatingModel.get_ratings_by_user(id)
            links = LinkModel.get_links()

            ratings_df = pd.DataFrame(ratings, columns=["movieId", "rating"])
            links_df = pd.DataFrame(links, columns=["movieId", "imdbId", "tmdbId"])

            ratings_df["tmdbId"] = ratings_df["movieId"].map(
                links_df.set_index("movieId")["tmdbId"]
            )

            ratings_df = ratings_df.drop(["movieId"], axis=1)

            ratings_df_json = ratings_df.to_dict(orient="records")

            return jsonify(ratings_df_json)
        except Exception as ex:
            return jsonify({"message": str(ex)}), 500
    else:
        response = jsonify({"message": "Unauthorized"})
        return response, 401


@main.route("/register", methods=["POST"])
def register_rating():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            tmdbId = request.json["tmdbId"]
            userId = request.json["userId"]
            rating = float(request.json["rating"])
            title = request.json["title"]
            year = request.json["year"]

            links_df = pd.DataFrame(
                LinkModel.get_links(), columns=["movieId", "imdbId", "tmdbId"]
            )

            # Verifica si el tmdbId existe en el DataFrame
            exists = tmdbId in links_df["tmdbId"].values
            movie_id = 0

            if exists:
                # El tmdbId existe en el DataFrame
                movie_id = links_df.loc[links_df["tmdbId"] == tmdbId, "movieId"].values[
                    0
                ]
            else:
                # El tmdbId no existe en el DataFrame
                movie_id = MovieModel.register_movie(title, year)
                LinkModel.register_link(movie_id, 0, tmdbId)

            affected_rows = RatingModel.register_rating(int(movie_id), userId, rating)

            if affected_rows == 1:
                return jsonify({"message": "Registro exitoso"})
            else:
                return jsonify({"message": "Error on insert"}), 500

        except Exception as ex:
            return jsonify({"message": str(ex)}), 500
    else:
        response = jsonify({"message": "Unauthorized"})
        return response, 401
