from flask import Blueprint, jsonify, request
import pandas as pd

# Entities
from models.entities.Movie import Movie

# Models
from models.MovieModel import MovieModel
from models.RatingModel import RatingModel
from models.LinkModel import LinkModel
from utils.MovieRecommender import MovieRecommender
from utils.Security import Security

main = Blueprint("recommendation_blueprint", __name__)


@main.route("/<id>")
def get_recommendations_by_user(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            user_input_ratings = RatingModel.get_ratings_by_user(id)
            movies = MovieModel.get_movies()
            ratings = RatingModel.get_ratings()
            links = LinkModel.get_links()

            movies_df = pd.DataFrame(movies, columns=["id", "title", "year"])
            ratings_df = pd.DataFrame(ratings, columns=["userId", "movieId", "rating"])
            links_df = pd.DataFrame(links, columns=["movieId", "imdbId", "tmdbId"])

            user_input_ratings_df = pd.DataFrame(
                user_input_ratings, columns=["movieId", "rating"]
            )

            # Fusiona los DataFrames en base a la columna 'movieId'
            merged_df = pd.merge(
                user_input_ratings_df,
                movies_df,
                left_on="movieId",
                right_on="id",
                how="inner",
            )

            # Selecciona solo las columnas 'title' y 'rating'
            user_input_ratings_df = merged_df[["title", "rating"]]

            # Renombrar la columna "id" a "movieId"
            movies_df = movies_df.rename(columns={"id": "movieId"})

            # Convierte la columna 'rating' a tipo float
            ratings_df["rating"] = ratings_df["rating"].astype(float)
            user_input_ratings_df["rating"] = user_input_ratings_df["rating"].astype(
                float
            )

            # Asegúrate de que userId sea de tipo int
            ratings_df["userId"] = ratings_df["userId"].astype(int)

            # Elimina las valoraciones hechas por el mismo usuario
            ratings_df = ratings_df[(ratings_df["userId"] != int(id))]

            # Instantiate MovieRecommender
            recommender = MovieRecommender(
                movies_df=movies_df, ratings_df=ratings_df, links_df=links_df
            )

            # Generar recomendaciones
            recommendations = recommender.generate_recommendations(
                user_input_ratings_df
            )

            # Obtener información adicional de las películas
            recommended_movies = links_df.loc[
                links_df["movieId"].isin(recommendations.head(10)["movieId"].tolist())
            ]

            # Convertir a formato JSON
            recommended_movies_json = recommended_movies.to_dict(orient="records")

            print(ratings_df.tail(20))

            return jsonify(recommended_movies_json)

        except Exception as ex:
            return jsonify({"message": str(ex)}), 500
    else:
        response = jsonify({"message": "Unauthorized"})
        return response, 401


@main.route("", methods=["POST"])
def get_recommendations():
    try:
        user_input_ratings = request.get_json()
        movies = MovieModel.get_movies()
        ratings = RatingModel.get_ratings()
        links = LinkModel.get_links()

        movies_df = pd.DataFrame(movies, columns=["id", "title", "year"])
        ratings_df = pd.DataFrame(ratings, columns=["userId", "movieId", "rating"])
        links_df = pd.DataFrame(links, columns=["movieId", "imdbId", "tmdbId"])

        user_input_ratings_df = pd.DataFrame(user_input_ratings)

        # Renombrar la columna "id" a "movieId"
        movies_df = movies_df.rename(columns={"id": "movieId"})

        # Elimina las valoraciones hechas por el mismo usuario
        ratings_df = ratings_df[(ratings_df["userId"] != id)]

        # Convierte la columna 'rating' a tipo float
        ratings_df["rating"] = ratings_df["rating"].astype(float)
        user_input_ratings_df["rating"] = user_input_ratings_df["rating"].astype(float)

        # Instantiate MovieRecommender
        recommender = MovieRecommender(
            movies_df=movies_df, ratings_df=ratings_df, links_df=links_df
        )

        # Generar recomendaciones
        recommendations = recommender.generate_recommendations(user_input_ratings_df)

        # Obtener información adicional de las películas
        recommended_movies = links_df.loc[
            links_df["movieId"].isin(recommendations.head(10)["movieId"].tolist())
        ]

        # Convertir a formato JSON
        recommended_movies_json = recommended_movies.to_dict(orient="records")

        return jsonify(recommended_movies_json)

    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
