import os

def normalize_database_url(url):
    if url and url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"): ]
    if url and url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"): ]
    return url

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///cupcake.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
