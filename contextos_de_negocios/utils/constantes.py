from datetime import datetime

import pytz
from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

load_dotenv()

SQLITE_TESTE = "sqlite+aiosqlite:///test_database.db"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_USER = os.getenv("DB_USER", "postgres")
DB_NAME = os.getenv("DB_NAME", "transacoes_bancarias")

SENTRY_DSN = os.getenv("SENTRY_DSN", default="")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default="30")
)

EMAIL_PRIMEIRO_USUARIO = os.getenv("EMAIL_PRIMEIRO_USUARIO")
SENHA_PRIMEIRO_USUARIO = os.getenv("SENHA_PRIMEIRO_USUARIO")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATA_AGORA = datetime.now(pytz.timezone("America/Sao_Paulo"))
