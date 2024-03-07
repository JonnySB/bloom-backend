import bcrypt

from lib.models.user import User


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
            )
            users.append(user)
        return users

    # When called with a user object, a corresponding record is created in the
    # db
    def add_user_to_db(self, user: User):
        self.connection.execute(
            """
            INSERT INTO users
            (first_name, last_name, username, email, hashed_password, avatar_url_string, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            [
                user.first_name,
                user.last_name,
                user.username,
                user.email,
                user.hashed_password,
                user.avatar_url_string,
                user.address,
            ],
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
    def get_user_by_id(self, user_id: int) -> User | bool:
        try:
            row = self.connection.execute(
                """
                SELECT * FROM users
                WHERE id = %s
                """,
                [user_id],
            )[0]
            return User(
                row["id"],
                row["first_name"],
                row["last_name"],
                row["username"],
                row["email"],
                "None",
                row["avatar_url_string"],
                row["address"],
            )
        except:
            return False

    def edit_user_details(
        self, user_id, first_name, last_name, username, email, address
    ):
        update_query = """UPDATE users SET first_name = %s, last_name = %s, username = %s, email = %s, address = %s WHERE id = %s"""
        result = self.connection.execute(
            update_query, [first_name, last_name, username, email, address, user_id]
        )
        print(result)
        return result
