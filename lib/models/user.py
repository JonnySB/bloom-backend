import bcrypt
import re

class User:
    def __init__(
        self,
        id: int | None,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        avatar_url_string: str = "",
        address: str = "",
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email if self._validate_email(email) else None
        self.hashed_password = self._hash_password(password) if self._validate_password(password) else None
        self.avatar_url_string = avatar_url_string
        self.address = address

    # ensure two objects with identical attributes will be found equal
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

    # return a nicely formatted string version of the User object
    def __repr__(self):
        return f"User: {self.id}, {self.first_name}, {self.last_name}, {self.username}, {self.email}, {self.avatar_url_string}, {self.address}"

    # When called with a plain text password, a hashed password is returned
    def _hash_password(self, password):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash

    @staticmethod
    def _validate_password(password):
        # Password must have at least 8 characters, one capital letter, one number, and one special character
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*()-_=+{};:,<.>]", password):
            return False
        return True
    
    @staticmethod
    def _validate_email(email):
        # Simple regex pattern to check email validity
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None