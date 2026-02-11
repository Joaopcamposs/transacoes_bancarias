import os
from typing import Generator

# ── Configurar env ANTES de qualquer import da aplicação ─────
TEST_DB_HOST: str = os.getenv("TEST_DB_HOST", "localhost")
TEST_DB_PORT: str = os.getenv("TEST_DB_PORT", "54322")
TEST_DB_USER: str = os.getenv("TEST_DB_USER", "postgres")
TEST_DB_PASSWORD: str = os.getenv("TEST_DB_PASSWORD", "postgres")
TEST_DB_NAME: str = os.getenv("TEST_DB_NAME", "transacoes_bancarias_test")

os.environ["DB_HOST"] = TEST_DB_HOST
os.environ["DB_PORT"] = TEST_DB_PORT
os.environ["DB_USER"] = TEST_DB_USER
os.environ["DB_PASSWORD"] = TEST_DB_PASSWORD
os.environ["DB_NAME"] = TEST_DB_NAME
os.environ["EMAIL_PRIMEIRO_USUARIO"] = "admin@email.com"
os.environ["SENHA_PRIMEIRO_USUARIO"] = "1234"
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt-signing"
os.environ["ALGORITHM"] = "HS256"

TEST_DATABASE_URL_SYNC: str = (
    f"postgresql+psycopg2://{TEST_DB_USER}:{TEST_DB_PASSWORD}"
    f"@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)

# ── Imports que dependem das env vars ────────────────────────
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402

from tests.mocks import (  # noqa: E402
    mock_client,
    mock_client_gen,
    mock_user_api,
    mock_bank_account,
    mock_user_gen,
    mock_bank_account_gen,
    mock_bank_transaction,
    mock_bank_transaction_gen,
)


@pytest.fixture(scope="session")
def client_api() -> Generator[TestClient, None, None]:
    """Cria o TestClient uma vez por sessão. Limpa o banco antes para garantir estado limpo."""
    # Dropa todas as tabelas para forçar o lifespan a recriar tudo do zero
    sync_engine = create_engine(TEST_DATABASE_URL_SYNC)
    with sync_engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()
    sync_engine.dispose()

    from infra.database import reset_engine

    reset_engine()

    from business_contexts.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clean_tables() -> Generator[None, None, None]:
    """Limpa tabelas antes de cada teste, preservando o usuário admin criado pelo lifespan."""
    sync_engine = create_engine(TEST_DATABASE_URL_SYNC)
    with sync_engine.connect() as conn:
        conn.execute(text("DELETE FROM bank_transaction"))
        conn.execute(text("DELETE FROM bank_account"))
        conn.execute(text("DELETE FROM client"))
        conn.execute(text("""DELETE FROM "user" WHERE email != 'admin@email.com'"""))
        conn.commit()
    sync_engine.dispose()
    yield
