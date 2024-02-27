import bcrypt

from lib.models.user import User


# Space constructs with an: id, name, description, price and user_id
def test_user_constructs():
    user = User(1, "John", "Doe", "jdoe", "jdoe@email.com", "Password123!")
    assert user.id == 1
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.username == "jdoe"
    assert user.email == "jdoe@email.com"
    # assert that hashed password (although different) is found to be equal
    assert bcrypt.checkpw("Password123!".encode("utf-8"), user.hashed_password)


# test the correct string representation is printed for the User object
# Note, hashed_password not included in str representation
def test_user_format():
    user = User(1, "John", "Doe", "jdoe", "jdoe@email.com", "Password123!")
    assert str(user) == "User: 1, John, Doe, jdoe, jdoe@email.com, , , []"


# tests two User objects with the same data are found equal
def test_identical_users():
    user1 = User(1, "John", "Doe", "jdoe", "jdoe@email.com", "Password123!")
    user2 = User(1, "John", "Doe", "jdoe", "jdoe@email.com", "Password123!")
    assert user1 == user2
