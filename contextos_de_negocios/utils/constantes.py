from dotenv import load_dotenv
import os

load_dotenv()

SQLITE_URL = "sqlite+aiosqlite:///database.db"

DATABASE_URI = os.getenv("DATABASE_URI")
SENTRY_DSN = os.getenv("SENTRY_DSN", default="")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default="30")
)

SENHA_PRIMEIRO_USUARIO = os.getenv("SENHA_PRIMEIRO_USUARIO")
