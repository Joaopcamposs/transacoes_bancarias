from dataclasses import dataclass
from decimal import Decimal
from random import randint
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from business_contexts.utils.base_types import CPF
from business_contexts.utils.constants import FIRST_USER_EMAIL, FIRST_USER_PASSWORD


@dataclass
class MockUserAPI:
    """Mock de usuário autenticado para testes de API."""

    id: str
    name: str
    email: str
    password: str
    is_admin: bool
    is_active: bool
    token: str


@dataclass
class MockClient:
    """Mock de cliente criado via API."""

    id: str
    name: str
    cpf: str


@dataclass
class MockBankAccount:
    """Mock de conta bancária criada via API."""

    id: str
    account_number: str
    balance: str
    client_cpf: str


def _auth_headers(token: str) -> dict[str, str]:
    """Retorna headers de autenticação."""
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def mock_user_api(client_api: TestClient) -> MockUserAPI:
    """Cria um usuário admin via API e retorna seus dados com token JWT."""
    user_data = {
        "name": "Admin",
        "email": FIRST_USER_EMAIL,
        "password": FIRST_USER_PASSWORD,
        "is_admin": True,
        "is_active": True,
    }

    # Primeiro faz login pra pegar token — o lifespan já criou o admin
    # Então cria via API se não existir
    login_resp = client_api.post(
        "api/token",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    if login_resp.status_code != 200:
        raise RuntimeError(
            f"Login falhou ({login_resp.status_code}): {login_resp.text}"
        )

    token = login_resp.json()["access_token"]

    me_resp = client_api.get("api/usuario/me", headers=_auth_headers(token))
    me = me_resp.json()

    return MockUserAPI(
        id=me["id"],
        name=me["name"],
        email=me["email"],
        password=user_data["password"],
        is_admin=me["is_admin"],
        is_active=me["is_active"],
        token=token,
    )


@pytest.fixture(scope="function")
def mock_client_gen() -> dict:
    """Gera dados de cliente para teste."""
    return {"name": "Cliente Teste", "cpf": CPF.generate()}


@pytest.fixture(scope="function")
def mock_client(
    client_api: TestClient, mock_user_api: MockUserAPI, mock_client_gen: dict
) -> MockClient:
    """Cria um cliente via API e retorna os dados."""
    resp = client_api.post(
        "api/cliente",
        json=mock_client_gen,
        headers=_auth_headers(mock_user_api.token),
    )
    assert resp.status_code == 200, f"Falha ao criar mock_client: {resp.text}"
    body = resp.json()

    return MockClient(id=body["id"], name=body["name"], cpf=body["cpf"])


@pytest.fixture(scope="function")
def mock_bank_account_gen() -> dict:
    """Gera dados de conta bancária para teste."""
    return {
        "account_number": str(randint(100000, 999999)),
        "balance": "0.00",
        "client_cpf": CPF.generate(),
    }


@pytest.fixture(scope="function")
def mock_bank_account(
    client_api: TestClient, mock_user_api: MockUserAPI, mock_client: MockClient
) -> Callable[..., MockBankAccount]:
    """Factory fixture que cria contas bancárias via API."""

    def _create(
        account_number: str | None = None, balance: Decimal | None = None
    ) -> MockBankAccount:
        data = {
            "account_number": account_number or str(randint(100000, 999999)),
            "balance": str(balance or Decimal("0.00")),
            "client_cpf": mock_client.cpf,
        }
        resp = client_api.post(
            "api/conta_bancaria",
            json=data,
            headers=_auth_headers(mock_user_api.token),
        )
        assert resp.status_code == 200, f"Falha ao criar mock_bank_account: {resp.text}"
        body = resp.json()
        return MockBankAccount(
            id=body["id"],
            account_number=body["account_number"],
            balance=body.get("balance", data["balance"]),
            client_cpf=mock_client.cpf,
        )

    return _create


@pytest.fixture(scope="function")
def mock_user_gen() -> dict:
    """Gera dados de usuário para teste."""
    return {
        "name": "Usuário Teste",
        "email": "joao@email.com",
        "password": "1234",
        "is_admin": False,
        "is_active": True,
    }


@pytest.fixture(scope="function")
def mock_bank_transaction_gen() -> dict:
    """Gera dados de transação bancária para teste."""
    return {
        "type": "deposit",
        "amount": 100.00,
        "account_number": "1234",
    }


@pytest.fixture(scope="function")
def mock_bank_transaction(
    client_api: TestClient, mock_user_api: MockUserAPI
) -> Callable[..., dict]:
    """Factory fixture que cria transações bancárias via API."""

    def _create(
        type: str = "deposit",
        amount: float = 100.00,
        account_number: str = "1234",
        destination_account_number: str = "",
    ) -> dict:
        data: dict = {
            "type": type,
            "amount": amount,
            "account_number": account_number,
        }
        if destination_account_number:
            data["destination_account_number"] = destination_account_number

        resp = client_api.post(
            "api/transacao_bancaria",
            json=data,
            headers=_auth_headers(mock_user_api.token),
        )
        assert resp.status_code == 200, (
            f"Falha ao criar mock_bank_transaction: {resp.text}"
        )
        return resp.json()

    return _create
