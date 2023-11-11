import pandas as pd
from math import sqrt


class MovieRecommender:
    def __init__(self, movies_df, ratings_df, links_df):
        self.movies_df = movies_df
        self.ratings_df = ratings_df
        self.links_df = links_df

    def filter_data(self, userInput):
        inputMovies = pd.DataFrame(userInput)
        inputId = self.movies_df[
            self.movies_df["title"].isin(inputMovies["title"].tolist())
        ]
        inputMovies = pd.merge(inputId, inputMovies)
        inputMovies = inputMovies.drop("year", axis=1)

        userSubset = self.ratings_df[
            self.ratings_df["movieId"].isin(inputMovies["movieId"].tolist())
        ]
        return inputMovies, userSubset

    def calculate_correlation(self, inputMovies, userSubset):
        userSubsetGroup = userSubset.groupby(["userId"])
        userSubsetGroup = sorted(userSubsetGroup, key=lambda x: len(x[1]), reverse=True)
        userSubsetGroup = userSubsetGroup[0:100]

        pearsonCorrelationDict = {}
        for (userId,), group in userSubsetGroup:
            group = group.sort_values(by="movieId")
            inputMovies = inputMovies.sort_values(by="movieId")
            nRatings = len(group)
            temp_df = inputMovies[
                inputMovies["movieId"].isin(group["movieId"].tolist())
            ]
            tempRatingList = temp_df["rating"].tolist()
            tempGroupList = group["rating"].tolist()

            Sxx = sum([i**2 for i in tempRatingList]) - pow(
                sum(tempRatingList), 2
            ) / float(nRatings)
            Syy = sum([i**2 for i in tempGroupList]) - pow(
                sum(tempGroupList), 2
            ) / float(nRatings)
            Sxy = sum(i * j for i, j in zip(tempRatingList, tempGroupList)) - sum(
                tempRatingList
            ) * sum(tempGroupList) / float(nRatings)

            if Sxx != 0 and Syy != 0:
                pearsonCorrelationDict[userId] = Sxy / sqrt(Sxx * Syy)
            else:
                pearsonCorrelationDict[userId] = 0

        pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient="index")
        pearsonDF.columns = ["similarityIndex"]
        pearsonDF["userId"] = pearsonDF.index
        pearsonDF.index = range(len(pearsonDF))

        return pearsonDF

    def generate_recommendations(self, userInput):
        # Filtrar datos
        inputMovies, userSubset = self.filter_data(userInput)

        # Calcular correlación
        pearsonDF = self.calculate_correlation(inputMovies, userSubset)

        # Obtener usuarios similares y calcular recomendaciones
        topUsers = pearsonDF.sort_values(by="similarityIndex", ascending=False)[0:50]
        topUsersRating = topUsers.merge(
            self.ratings_df, left_on="userId", right_on="userId", how="inner"
        )
        topUsersRating["weightedRating"] = (
            topUsersRating["similarityIndex"] * topUsersRating["rating"]
        )

        tempTopUsersRating = topUsersRating.groupby("movieId").sum()[
            ["similarityIndex", "weightedRating"]
        ]
        tempTopUsersRating.columns = ["sum_similarityIndex", "sum_weightedRating"]

        recommendation_df = pd.DataFrame()
        recommendation_df["weighted average recommendation score"] = (
            tempTopUsersRating["sum_weightedRating"]
            / tempTopUsersRating["sum_similarityIndex"]
        )
        recommendation_df["movieId"] = tempTopUsersRating.index
        recommendation_df = recommendation_df.sort_values(
            by="weighted average recommendation score", ascending=False
        )

        return recommendation_df
