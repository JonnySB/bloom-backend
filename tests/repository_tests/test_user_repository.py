from lib.models.user import User
from lib.repositories.user_repository import UserRepository


# tests all users retuned when called
def test_get_all_users(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    users = repository.get_all_users()
    assert users == [
        User(
            1,
            "user",
            "1",
            "user1",
            "user1@email.com",
            "Password123!",
            "test_image1.png",
            "test_address1",
        ),
        User(
            2,
            "user",
            "2",
            "user2",
            "user2@email.com",
            "Password123!",
            "test_image2.png",
            "test_address2",
        ),
        User(
            3,
            "user",
            "3",
            "user3",
            "user3@email.com",
            "Password123!",
            "test_image3.png",
            "test_address3",
        ),
        User(
            4,
            "user",
            "4",
            "user4",
            "user4@email.com",
            "Password123!",
            "test_image4.png",
            "test_address4",
        ),
        User(
            5,
            "user",
            "5",
            "user5",
            "user5@email.com",
            "Password123!",
            "test_image5.png",
            "test_address5",
        ),
        User(
            6,
            "user",
            "6",
            "user6",
            "user6@email.com",
            "Password123!",
            "test_image6.png",
            "test_address5",
        ),
    ]


# tests a correcponding record is crated in the database when called with a
# User object
def test_create_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    # id updated to correct (7) when reconstructed from db
    user = User(None, "user", "7", "user7", "user7@email.com", "Password123!")
    repository.add_user_to_db(user)

    users = repository.get_all_users()
    assert users == [
        User(
            1,
            "user",
            "1",
            "user1",
            "user1@email.com",
            "Password123!",
            "test_image1.png",
            "test_address1",
        ),
        User(
            2,
            "user",
            "2",
            "user2",
            "user2@email.com",
            "Password123!",
            "test_image2.png",
            "test_address2",
        ),
        User(
            3,
            "user",
            "3",
            "user3",
            "user3@email.com",
            "Password123!",
            "test_image3.png",
            "test_address3",
        ),
        User(
            4,
            "user",
            "4",
            "user4",
            "user4@email.com",
            "Password123!",
            "test_image4.png",
            "test_address4",
        ),
        User(
            5,
            "user",
            "5",
            "user5",
            "user5@email.com",
            "Password123!",
            "test_image5.png",
            "test_address5",
        ),
        User(
            6,
            "user",
            "6",
            "user6",
            "user6@email.com",
            "Password123!",
            "test_image6.png",
            "test_address5",
        ),
        User(7, "user", "7", "user7", "user7@email.com", "Password123!"),
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

    user_id = repository.get_user_id_from_username_or_email("user5@email.com")
    assert user_id == 5


# tests that when called with correct password, the corresponding user id is
# returned
def test_correct_password_returns_user_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)
    user = User(None, "user", "7", "user7", "user7@email.com", "Password123!")

    repository.add_user_to_db(user)
    user_id = repository.check_username_or_email_and_password("user7", "Password123!")
    assert user_id == 7


# tests that when called with an incorrect password, returns false
def test_incorrect_password_returns_false(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)
    user = User(None, "user", "7", "user7", "user7@email.com", "Password123!")

    repository.add_user_to_db(user)
    is_valid_password = repository.check_username_or_email_and_password(
        "user7", "dawdawd"
    )
    assert is_valid_password == False


# tests when called with a specific user id, the corresponding user object is
# returned
def test_get_user_by_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    user_details = repository.get_user_by_id(3)
    assert user_details == User(
        3,
        "user",
        "3",
        "user3",
        "user3@email.com",
        "Password123!",
        "test_image3.png",
        "test_address3",
    )
