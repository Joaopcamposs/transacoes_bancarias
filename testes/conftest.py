import os

# Setar env de teste ANTES de qualquer import do projeto
os.environ["TEST_ENV"] = "true"

import pytest
from dataclasses import dataclass
from fastapi.testclient import TestClient

from contextos_de_negocios.utils.tipos_basicos import CPF
from contextos_de_negocios.servicos.executores.seguranca import criar_token
from contextos_de_negocios.utils.constantes import EMAIL_PRIMEIRO_USUARIO
from infra import start_mappers

# Inicializar mappers uma vez no nível de módulo
start_mappers()


@dataclass
class MockUsuarioAPI:
    nome: str
    email: str
    senha: str
    adm: bool
    ativo: bool
    token: str
    id: str | None = None


@pytest.fixture(scope="session")
def client_api():
    """Client síncrono para testes com Postgres."""
    import infra.banco_de_dados as db_module
    from contextos_de_negocios.main import app

    # Resetar engine para usar Postgres de teste
    db_module.ASYNC_ENGINE = None

    # Context manager necessário para executar o lifespan (cria tabelas e usuário)
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def mock_usuario_api():
    """Token para autenticação nos testes."""
    access_token = criar_token(data={"sub": EMAIL_PRIMEIRO_USUARIO})

    return MockUsuarioAPI(
        id=None,
        nome="Admin",
        email=EMAIL_PRIMEIRO_USUARIO,
        senha="1234",
        adm=True,
        ativo=True,
        token=access_token,
    )


@pytest.fixture(scope="function")
def mock_cliente_gen() -> dict:
    return {"nome": "Cliente Teste", "cpf": CPF.gerar()}


@pytest.fixture(scope="function")
def mock_usuario_gen() -> dict:
    return {
        "nome": "Usuário Teste",
        "email": f"teste_{CPF.gerar()[:8]}@email.com",
        "senha": "1234",
        "adm": False,
        "ativo": True,
    }


@pytest.fixture(scope="function")
def mock_conta_bancaria_gen() -> dict:
    from random import randint

    return {
        "numero_da_conta": str(randint(100000, 999999)),
        "saldo": "0.00",
        "cpf_cliente": CPF.gerar(),
    }


@pytest.fixture(scope="function")
def mock_transacao_bancaria_gen(mock_conta_bancaria_gen) -> dict:
    return {
        "tipo": "deposito",
        "valor": "100.00",
        "numero_da_conta": mock_conta_bancaria_gen["numero_da_conta"],
    }


def criar_cliente_teste(client_api, token: str, dados: dict = None):
    """Helper para criar cliente de teste via API."""
    from contextos_de_negocios.dominio.agregados.cliente import Cliente

    if dados is None:
        dados = {"nome": "Cliente Teste", "cpf": CPF.gerar()}

    response = client_api.post(
        "api/cliente",
        json=dados,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()

    return Cliente(id=data["id"], nome=data["nome"], cpf=data["cpf"])


@pytest.fixture(scope="function")
def mock_conta_bancaria(client_api, mock_usuario_api):
    """Factory para criar contas bancárias de teste via API."""
    from random import randint

    def _create(
        numero_da_conta: str = None, saldo: str = "0.00", cpf_cliente: str = None
    ):
        # Criar cliente primeiro se cpf não fornecido
        if cpf_cliente is None:
            cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
            cpf_cliente = cliente.cpf

        dados = {
            "numero_da_conta": numero_da_conta or str(randint(100000, 999999)),
            "saldo": saldo,
            "cpf_cliente": cpf_cliente,
        }

        response = client_api.post(
            "api/conta_bancaria",
            json=dados,
            headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
        )
        assert response.status_code == 200, f"Erro ao criar conta: {response.text}"
        return response.json()

    return _create


@pytest.fixture(scope="function")
def mock_transacao_bancaria(client_api, mock_usuario_api, mock_conta_bancaria):
    """Factory para criar transações de teste via API."""

    def _create(
        tipo: str = "deposito",
        valor: str = "100.00",
        numero_da_conta: str = None,
        numero_da_conta_destino: str = "",
    ):
        # Criar conta se não fornecida
        if numero_da_conta is None:
            conta = mock_conta_bancaria(saldo="1000.00")
            numero_da_conta = conta["numero_da_conta"]

        dados = {
            "tipo": tipo,
            "valor": valor,
            "numero_da_conta": numero_da_conta,
            "numero_da_conta_destino": numero_da_conta_destino,
        }

        response = client_api.post(
            "api/transacao_bancaria",
            json=dados,
            headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
        )
        assert response.status_code == 200, f"Erro ao criar transação: {response.text}"
        return response.json()

    return _create
