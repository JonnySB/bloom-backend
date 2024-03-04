import pytest, sys, random, py, pytest, os
from xprocess import ProcessStarter
from lib.database_connection import DatabaseConnection
from app import app


# # This fixture is used to create a database connection.
# @pytest.fixture
# def db_connection():
#     conn = DatabaseConnection(test_mode=True)
#     conn.connect()
#     return conn


# # This fixture starts the test server and makes it available to the tests.
# @pytest.fixture
# def test_web_address(xprocess):
#     python_executable = sys.executable
#     app_file = py.path.local(__file__).dirpath("../app.py")
#     port = str(random.randint(4000, 4999))

#     class Starter(ProcessStarter):
#         env = {"PORT": port, "APP_ENV": "test", **os.environ}
#         # pattern = r"\* Running on http:\/\/127\.0\.0\.1:5001"
#         timeout = 180  # Adjust this value as necessary
#         pattern = "[Dd]ebugger is active " # this one [Dd]ebugger is active pass locally 
#         args = [python_executable, app_file]

#     xprocess.ensure("flask_test_server", Starter)

#     yield f"localhost:{port}"

#     xprocess.getinfo("flask_test_server").terminate()


# # We'll also create a fixture for the client we'll use to make test requests.
# @pytest.fixture
# def web_client():
#     app.config["TESTING"] = True  # This gets us better errors
#     with app.test_client() as client:
#         yield client


import pytest, sys, random, py, pytest, os
from xprocess import ProcessStarter
from lib.database_connection import DatabaseConnection
from app import app


# This fixture is used to create a database connection.
@pytest.fixture
def db_connection():
    conn = DatabaseConnection(test_mode=True)
    conn.connect()
    return conn


# This fixture starts the test server and makes it available to the tests.
@pytest.fixture
def test_web_address(xprocess):
    python_executable = sys.executable
    app_file = py.path.local(__file__).dirpath("../app.py")
    port = str(random.randint(4000, 4999))

    class Starter(ProcessStarter):
        env = {"PORT": port, "APP_ENV": "test", **os.environ}
        pattern = "Debugger PIN"
        timeout = 180 
        args = [python_executable, app_file]

    xprocess.ensure("flask_test_server", Starter)

    yield f"localhost:{port}"

    xprocess.getinfo("flask_test_server").terminate()


# We'll also create a fixture for the client we'll use to make test requests.
@pytest.fixture
def web_client():
    app.config["TESTING"] = True  # This gets us better errors
    with app.test_client() as client:
        yield client