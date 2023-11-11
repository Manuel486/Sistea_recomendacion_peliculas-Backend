class User:
    def __init__(self, id, names, lastnames, email, password):
        self.id = id
        self.names = names
        self.lastnames = lastnames
        self.email = email
        self.password = password

    def to_JSON(self):
        return {
            "id": self.id,
            "names": self.names,
            "lastnames": self.lastnames,
            "email": self.email,
            "password": self.password,
        }
