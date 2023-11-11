class Movie:
    def __init__(self, id, title=None, year=None) -> None:
        self.id = id
        self.title = title
        self.year = year

    def to_JSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
        }
