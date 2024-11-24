import os

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine

from contextos_de_negocios.utils.constantes import SQLITE_TESTE
from contextos_de_negocios.main import app
from infra import start_mappers
from infra.banco_de_dados import mapper_registry, Base
from testes.mocks import (
    mock_cliente,
    mock_cliente_gen,
    mock_usuario_api,
    mock_conta_bancaria,
    mock_usuario_gen,
    mock_conta_bancaria_gen,
    mock_transacao_bancaria,
    mock_transacao_bancaria_gen,
)


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["TEST_ENV"] = "true"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def inicializar_banco_de_dados(test_engine):
    # start_mappers()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
def client_api():
    client_api_test = TestClient(app)
    return client_api_test


@pytest_asyncio.fixture(scope="session")
def test_engine():
    engine = create_async_engine(
        url=SQLITE_TESTE,
        isolation_level="SERIALIZABLE",
        future=True,
    )
    yield engine
    engine.dispose()


async def limpar_banco_de_dados(test_engine):
    # necessario adicionar as tabelas na ordem correta, manualmente
    lista_de_tabelas = [
        "usuario",
        "cliente",
        "transacao_bancaria",
        "conta_bancaria",
    ]

    async with test_engine.connect() as conn:
        transaction = await conn.begin()
        try:
            for table_name in lista_de_tabelas:
                # Reflete as tabelas
                table = Table(table_name, mapper_registry.metadata)
                # Executa o DELETE para limpar os dados
                await conn.execute(table.delete())
            await transaction.commit()
        except Exception as e:
            await transaction.rollback()
            print(f"Erro ao limpar a tabela {table_name}: {e}")


# Fixture de limpeza antes e depois de cada teste individual
@pytest_asyncio.fixture(scope="function", autouse=True)
async def limpador_de_banco_de_dados(test_engine):
    # Limpa o banco de dados antes de cada teste
    await limpar_banco_de_dados(test_engine)
    yield  # Executa o teste
