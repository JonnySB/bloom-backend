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
            "Tom",
            "Jones",
            "tee-jay",
            "tjones@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "test_address1",
        ),
        User(
            2,
            "Jane",
            "Smith",
            "jane95",
            "jsmith@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "test_address2",
        ),
        User(
            3,
            "Jilly",
            "Smith",
            "sm1thi",
            "jsmith2@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
            "test_address3",
        ),
        User(
            4,
            "Barbra",
            "Banes",
            "barn-owl58",
            "bbanes@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "test_address4",
        ),
        User(
            5,
            "Alice",
            "Lane",
            "laney",
            "alane@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "test_address5",
        ),
    ]


# tests a correcponding record is crated in the database when called with a
# User object
def test_create_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    # id updated to correct (7) when reconstructed from db
    user = User(None, "user", "6", "user6", "user6@email.com", "Password123!")
    repository.add_user_to_db(user)

    users = repository.get_all_users()
    assert users == [
        User(
            1,
            "Tom",
            "Jones",
            "tee-jay",
            "tjones@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "test_address1",
        ),
        User(
            2,
            "Jane",
            "Smith",
            "jane95",
            "jsmith@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "test_address2",
        ),
        User(
            3,
            "Jilly",
            "Smith",
            "sm1thi",
            "jsmith2@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
            "test_address3",
        ),
        User(
            4,
            "Barbra",
            "Banes",
            "barn-owl58",
            "bbanes@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "test_address4",
        ),
        User(
            5,
            "Alice",
            "Lane",
            "laney",
            "alane@email.com",
            "Password123!",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "test_address5",
        ),
        User(6, "user", "6", "user6", "user6@email.com", "Password123!"),
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

    user_id = repository.get_user_id_from_username_or_email("tee-jay")
    assert user_id == 1


# tests that when called with a valid email, the corresponding id is returned
def test_find_user_by_email(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)

    user_id = repository.get_user_id_from_username_or_email("tjones@email.com")
    assert user_id == 1


# tests that when called with correct password, the corresponding user id is
# returned
def test_correct_password_returns_user_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)
    user = User(None, "user", "6", "user6", "user6@email.com", "Password123!")

    repository.add_user_to_db(user)
    user_id = repository.check_username_or_email_and_password("user6", "Password123!")
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
        3,
        "Jilly",
        "Smith",
        "sm1thi",
        "jsmith2@email.com",
        "Password123!",
        "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
        "test_address3",
    )


def test_edit_user_details(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = UserRepository(db_connection)
    repository.edit_user_details(1, "Tom", "jones", "tee-jay", "tjones@email.com", "test_address1")
    updated_user = repository.get_user_by_id(1)
    assert updated_user.first_name == "Tom"
    assert updated_user.last_name == "jones"
    assert updated_user.username == "tee-jay"
    assert updated_user.email == "tjones@email.com"
    assert updated_user.address == "test_address1"