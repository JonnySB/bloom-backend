import bcrypt


class User:
    def __init__(
        self,
        id: int | None,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        avatar_url_string: str = "default_image",
        address: str = "",
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.hashed_password = self._hash_password(password)
        self.avatar_url_string = avatar_url_string
        self.address = address

    # ensure two object with identical attrs will be found equal
    def __eq__(self, other):
        # includes all items apart from hashed password
        return all(
            [
                self.id == other.id,
                self.first_name == other.first_name,
                self.last_name == other.last_name,
                self.username == other.username,
                self.email == other.email,
                self.avatar_url_string == other.avatar_url_string,
                self.address == other.address,
            ]
        )

    # return nicely formatted string version of User object
    def __repr__(self):
        return f"User: {self.id}, {self.first_name}, {self.last_name}, {self.username}, {self.email}, {self.avatar_url_string}, {self.address}"

    # When called with a plain text password, a hashed password is returned
    def _hash_password(self, password):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash
