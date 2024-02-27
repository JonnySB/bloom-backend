from lib.models.user import User
import bcrypt

"""
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.hashed_password = self._hash_password(password)
        self.avatar_url_string = ""
        self.address = ""
        self.plants = []

"""


class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    # When called, all users are returned as a list of User objects from the db
    def get_all_users(self) -> list[User]:
        users = []
        rows = self.connection.execute("SELECT * FROM users;")

        for row in rows:
            user = User(
                row["id"],
                row["first_name"],
                row["last_name"],
                row["username"],
                row["email"],
                "None",
                row["avatar_url_string"],
                row["address"],
                row["plants"],
            )
            users.append(user)
        return users

    # When called with a user object, a corresponding record is created in the
    # db
    def add_user_to_db(self, user: User):
        self.connection.execute(
            """
            INSERT INTO users
            (username, email, hashed_password)
            VALUES (%s, %s, %s);
            """,
            [user.username, user.email, user.hashed_password],
        )

    # When called with either a username or email, the corresponding user id
    # is returned from the database. If not found, return False
    def get_user_id_from_username_or_email(self, username_or_email: str) -> int:
        rows = self.connection.execute(
            """
            SELECT * FROM users
            WHERE username = %s OR email = %s;
            """,
            [username_or_email, username_or_email],
        )
        if len(rows) == 0:
            return False
        row = rows[0]
        return row["id"]

    # When called with a username / email and password, gets user_id from db.
    # Then uses user_id to get hashed_password from db and check valid. If
    # valid, return user_id, otherwiese return False
    def check_username_or_email_and_password(
        self, username_or_email: str, password: str
    ) -> int:
        user_id = self.get_user_id_from_username_or_email(username_or_email)
        if not user_id:
            return False

        hashed_database_pw = self.connection.execute(
            """
            SELECT hashed_password
            FROM users
            WHERE id = %s
            """,
            [user_id],
        )[0]["hashed_password"]

        is_valid_password = bcrypt.checkpw(password.encode("utf-8"), hashed_database_pw)
        return user_id if is_valid_password else False

    # When called with user id, get corresponding data from db and return as
    # User object
    def get_user_by_id(self, user_id: int) -> User:
        rows = self.connection.execute(
            """
            SELECT * FROM users
            WHERE id = %s
            """,
            [user_id],
        )[0]
        return User(rows["id"], rows["username"], rows["email"], "None")
