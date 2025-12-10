import json
from pathlib import Path

from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordBearer

load_dotenv()


def get_config_value(key: str, default: str = ""):
    """
    Retorna o valor da variável de configuração buscando na seguinte ordem:
    1. Variáveis de ambiente (.env ou docker env)
    2. Arquivo secrets.json
    3. Valor default (caso informado)
    """
    return os.getenv(key.upper()) or config.get(key.upper()) or default


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
with open(BASE_DIR / "infra/secrets.json") as f:
    config = json.load(f)

SQLITE_TESTE = "sqlite+aiosqlite:///test_database.db"

DB_HOST = get_config_value("DB_HOST", "localhost")
DB_PASSWORD = get_config_value("DB_PASSWORD", "postgres")
DB_USER = get_config_value("DB_USER", "postgres")
DB_NAME = get_config_value("DB_NAME", "transacoes_bancarias")

SENTRY_DSN = get_config_value("SENTRY_DSN", default="")

SECRET_KEY = get_config_value("SECRET_KEY")
ALGORITHM = get_config_value("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    get_config_value("ACCESS_TOKEN_EXPIRE_MINUTES", default="30")
)

EMAIL_PRIMEIRO_USUARIO = get_config_value("EMAIL_PRIMEIRO_USUARIO")
SENHA_PRIMEIRO_USUARIO = get_config_value("SENHA_PRIMEIRO_USUARIO")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
