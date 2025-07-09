import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if USE_SQLITE:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        SQLITE_DB_PATH = os.path.join(BASE_DIR, '..', 'wsquare.db')  # adjust path if needed
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"

        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {'check_same_thread': False}
        }
    else:
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
