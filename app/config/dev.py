"""Dev config."""

SECRET_KEY = "my_precious"
SECURITY_PASSWORD_SALT = "my_precious_two"

# For showing debug info.
DEBUG = True

# Get environment variables from os.
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'jwt_auth_db'
DB_USER = 'postgres'
DB_PASS = 'root'

# Database connection string.
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

# http://flask-sqlalchemy.pocoo.org/2.3/config/
SQLALCHEMY_TRACK_MODIFICATIONS = False

SMTP_EMAIL_SERVER = 'smtp.mail.eu-west-1.awsapps.com'
SENDER_EMAIL_ADDRESS = 'noreply@whitespacerenovation.com'
SENDER_EMAIL_PASS = 'EtDj!X&/uwrJ6!x@'
RECEIVER_EMAIL_ADDRESS = 'mijovic95.petar@gmail.com'
