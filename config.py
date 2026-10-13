
import os


def normalize_database_url(url):
    if url and url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url and url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


class Config:
    APP_ENV = os.getenv("APP_ENV", "development").lower()

    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        if APP_ENV == "production":
            raise RuntimeError(
                "Configure SECRET_KEY no ambiente de produção."
            )
        SECRET_KEY = "dev-secret-change-me"

    DATABASE_URL = os.getenv("DATABASE_URL")
    if APP_ENV == "production" and not DATABASE_URL:
        raise RuntimeError(
            "Configure DATABASE_URL no ambiente de produção."
        )

    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        DATABASE_URL or "sqlite:///cupcake.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
