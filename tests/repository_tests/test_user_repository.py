from lib.models.user import User
from lib.repositories.user_repository import UserRepository


# tests all users retuned when called
def test_get_all_users(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    users = repository.get_all_users()
    assert users == [
        User(1, "user", "1", "user_1", "user1@email.com", "Password123!"),
        User(2, "user", "2", "user_2", "user2@email.com", "Password123!"),
        User(3, "user", "3", "user_3", "user3@email.com", "Password123!"),
        User(4, "user", "4", "user_4", "user4@email.com", "Password123!"),
        User(5, "user", "5", "user_5", "user5@email.com", "Password123!"),
    ]


# tests a correcponding record is crated in the database when called with a
# User object
def test_create_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    # id updated to correct (6) when reconstructed from db
    user = User(None, "user", "6", "user_6", "user6@email.com", "Password123!")
    repository.add_user_to_db(user)

    users = repository.get_all_users()
    assert users == [
        User(1, "user", "1", "user_1", "user1@email.com", "Password123!"),
        User(2, "user", "2", "user_2", "user2@email.com", "Password123!"),
        User(3, "user", "3", "user_3", "user3@email.com", "Password123!"),
        User(4, "user", "4", "user_4", "user4@email.com", "Password123!"),
        User(5, "user", "5", "user_5", "user5@email.com", "Password123!"),
        User(6, "user", "6", "user_6", "user6@email.com", "Password123!"),
    ]


# tests when called with invalid username / email, returns False
def test_find_user_invalid(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    # Finds user by username or email
    is_valid_user = repository.get_user_id_from_username_or_email("nasadk")
    assert is_valid_user == False


# tests that when called with a valid username, the corresponding id is returned
def test_find_user_by_username(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    user_id = repository.get_user_id_from_username_or_email("user1")
    assert user_id == 1


# tests that when called with a valid email, the corresponding id is returned
def test_find_user_by_email(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    user_id = repository.get_user_id_from_username_or_email("user5@user.com")
    assert user_id == 5


# tests that when called with correct password, the corresponding user id is
# returned
def test_correct_password_returns_user_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)
    user = User(None, "user", "6", "user6", "user6@email.com", "Password123!")

    repository.add_user_to_db(user)
    user_id = repository.check_username_or_email_and_password("user6", "Password")
    assert user_id == 6


# tests that when called with an incorrect password, returns false
def test_incorrect_password_returns_false(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)
    user = User(None, "user", "6", "user6", "user6@email.com", "Password123!")

    repository.add_user_to_db(user)
    is_valid_password = repository.check_username_or_email_and_password(
        "user6", "dawdawd"
    )
    assert is_valid_password == False


# tests when called with a specific user id, the corresponding user object is
# returned
def test_get_user_by_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    user_details = repository.get_user_by_id(3)
    assert user_details == User(
        3, "user", "3", "user_3", "user3@email.com", "Password123!"
    )
