from dotenv import load_dotenv
import os

load_dotenv()

SQLITE_URL = "sqlite+aiosqlite:///database.db"
SQLITE_TESTE = "sqlite+aiosqlite:///test_database.db"

DATABASE_URI = os.getenv("DATABASE_URI")
SENTRY_DSN = os.getenv("SENTRY_DSN", default="")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default="30")
)

EMAIL_PRIMEIRO_USUARIO = os.getenv("EMAIL_PRIMEIRO_USUARIO")
SENHA_PRIMEIRO_USUARIO = os.getenv("SENHA_PRIMEIRO_USUARIO")
