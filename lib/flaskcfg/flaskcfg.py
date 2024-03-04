class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/BLOOM'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/BLOOM_test'
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens in the forms for tests