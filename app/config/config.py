import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    db_name = os.environ.get("POSTGRES_DB")
    db_host = os.environ.get("POSTGRES_HOST")
    db_user = os.environ.get("POSTGRES_USER")
    db_port = os.environ.get("POSTGRES_PORT")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_dsn = os.environ.get("POSTGRES_DSN")


settings = Settings()
