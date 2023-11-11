class Link:
    def __init__(self, id, movieId=None, imdbId=None, tmdbId=None) -> None:
        self.id = id
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId

    def to_JSON(self):
        return {
            "id": self.id,
            "movieId": self.movieId,
            "imdbId": self.imdbId,
            "tmdbId": self.tmdbId,
        }
