import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from contextos_de_negocios.utils.constantes import SQLITE_TESTE
from infra.database import get_db, Base
from contextos_de_negocios.main import app
from testes import override_get_db
from testes.mocks import (
    mock_cliente,
    mock_cliente_gen,
    mock_usuario_api,
    mock_conta_bancaria,
)


@pytest.fixture
def client_api():
    app.dependency_overrides[get_db] = override_get_db
    client_api_test = TestClient(app)
    return client_api_test


@pytest_asyncio.fixture(scope="session")
def postgres_test_engine():
    engine = create_async_engine(
        url=SQLITE_TESTE,
        isolation_level="SERIALIZABLE",
        future=True,
    )
    yield engine
    engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def session_factory(postgres_test_engine):
    yield sessionmaker(
        expire_on_commit=False, bind=postgres_test_engine, class_=AsyncSession
    )


async def limpar_banco_de_dados(postgres_test_engine):
    testing_session = sessionmaker(
        expire_on_commit=False, bind=postgres_test_engine, class_=AsyncSession
    )
    # necessario adicionar as tabelas na ordem correta, manualmente
    lista_de_tabelas = [
        "usuario",
        "cliente",
        "transacao_bancaria",
        "conta_bancaria",
    ]
    async with testing_session() as session:
        for table_name in lista_de_tabelas:
            table = Table(table_name, Base().metadata, autoload=True)
            try:
                await session.execute(table.delete())
            except Exception as e:
                print(e)
        await session.commit()


# Fixture de limpeza antes e depois de cada teste individual
@pytest_asyncio.fixture(scope="function", autouse=True)
async def limpador_de_banco_de_dados(postgres_test_engine):
    # Limpa o banco de dados antes de cada teste
    await limpar_banco_de_dados(postgres_test_engine)
    yield  # Executa o teste
    # Limpa o banco de dados após o teste
    await limpar_banco_de_dados(postgres_test_engine)
