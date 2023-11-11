class Rating:
    def __init__(self, id, movieId=None, userId=None, rating=None) -> None:
        self.id = id
        self.movieId = movieId
        self.userId = userId
        self.rating = rating

    def to_JSON(self):
        return {
            "id": self.id,
            "movieId": self.movieId,
            "userId": self.userId,
            "rating": self.rating,
        }

    def to_JSON_2_variables(self):
        return {"movieId": self.movieId, "rating": self.rating}
