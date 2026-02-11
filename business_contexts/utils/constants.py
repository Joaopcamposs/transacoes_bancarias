import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()


def get_config_value(key: str, default: str = "") -> str:
    """
    Retorna o valor da variável de configuração buscando na seguinte ordem:
    1. Variáveis de ambiente (.env ou docker env)
    2. Arquivo secrets.json
    3. Valor default (caso informado)
    """
    return os.getenv(key.upper()) or config.get(key.upper()) or default


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
with open(BASE_DIR / "infra/secrets.json") as f:
    config: dict[str, str] = json.load(f)

DB_HOST: str = get_config_value("DB_HOST", "localhost")
DB_PORT: int = int(get_config_value("DB_PORT", "54321"))
DB_PASSWORD: str = get_config_value("DB_PASSWORD", "postgres")
DB_USER: str = get_config_value("DB_USER", "postgres")
DB_NAME: str = get_config_value("DB_NAME", "transacoes_bancarias")

SENTRY_DSN: str = get_config_value("SENTRY_DSN", default="")

SECRET_KEY: str = get_config_value("SECRET_KEY")
ALGORITHM: str = get_config_value("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    get_config_value("ACCESS_TOKEN_EXPIRE_MINUTES", default="30")
)

FIRST_USER_EMAIL: str = get_config_value("EMAIL_PRIMEIRO_USUARIO")
FIRST_USER_PASSWORD: str = get_config_value("SENHA_PRIMEIRO_USUARIO")
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/token")
