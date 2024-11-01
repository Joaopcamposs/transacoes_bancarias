import asyncio
from decimal import Decimal

import pytest


@pytest.mark.asyncio
async def teste_deposito(client_api, mock_usuario_api, mock_conta_bancaria):
    await mock_conta_bancaria(numero_da_conta="123")

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "deposito",
            "valor": 100.00,
            "numero_da_conta": "123",
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api.status_code == 200, resposta_api.text

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=123",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "100.00"


@pytest.mark.asyncio
async def teste_saque(client_api, mock_usuario_api, mock_conta_bancaria):
    await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "saque",
            "valor": 50.00,
            "numero_da_conta": "123",
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api.status_code == 200, resposta_api.text

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=123",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "50.00"


@pytest.mark.asyncio
async def teste_transferencia(client_api, mock_usuario_api, mock_conta_bancaria):
    await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(50.00))
    await mock_conta_bancaria(numero_da_conta="456", saldo=Decimal(0.00))

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "transferencia",
            "valor": 30.00,
            "numero_da_conta": "123",
            "numero_da_conta_destino": "456",
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api.status_code == 200, resposta_api.text

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=123",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "20.00"

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=456",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "30.00"


async def requisicoes_concorrentes(
    client_api,
    mock_usuario_api,
    tipo: str,
    valor: float,
    numero_da_conta: str,
    numero_da_conta_destino: str | None = None,
) -> dict:
    corpo_da_requisicao = {
        "tipo": tipo,
        "valor": valor,
        "numero_da_conta": numero_da_conta,
    }
    if numero_da_conta_destino:
        corpo_da_requisicao.update({"numero_da_conta_destino": numero_da_conta_destino})

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json=corpo_da_requisicao,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    return resposta_api.json()


@pytest.mark.asyncio
async def teste_concorrencia_deposito_e_saque(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(0.00))

    transacoes = [
        requisicoes_concorrentes(
            client_api, mock_usuario_api, "deposito", 50.00, "123"
        ),
        requisicoes_concorrentes(client_api, mock_usuario_api, "saque", 30.00, "123"),
    ]

    # Executando atualizações concorrentes
    resultados = await asyncio.gather(*transacoes)

    # Verificando se as atualizações foram aplicadas corretamente
    assert len(resultados) == 2

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=123",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "20.00"


@pytest.mark.asyncio
async def teste_concorrencia_deposito_e_transferencia(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(0.00))
    await mock_conta_bancaria(numero_da_conta="456", saldo=Decimal(0.00))

    transacoes = [
        requisicoes_concorrentes(
            client_api, mock_usuario_api, "deposito", 100.00, "123"
        ),
        requisicoes_concorrentes(
            client_api, mock_usuario_api, "transferencia", 50.00, "123", "456"
        ),
    ]

    # Executando atualizações concorrentes
    resultados = await asyncio.gather(*transacoes)

    # Verificando se as atualizações foram aplicadas corretamente
    assert len(resultados) == 2

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=123",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "50.00"

    resposta_api_conta_2 = client_api.get(
        "api/conta_bancarias?numero_da_conta=456",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta_2.status_code == 200, resposta_api_conta_2.text
    assert resposta_api_conta_2.json()[0]["saldo"] == "50.00"


@pytest.mark.asyncio
async def teste_concorrencia_transferencias(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))
    await mock_conta_bancaria(numero_da_conta="456", saldo=Decimal(0.00))
    await mock_conta_bancaria(numero_da_conta="789", saldo=Decimal(0.00))

    transacoes = [
        requisicoes_concorrentes(
            client_api, mock_usuario_api, "transferencia", 20.00, "123", "456"
        ),
        requisicoes_concorrentes(
            client_api, mock_usuario_api, "transferencia", 10.00, "456", "789"
        ),
    ]

    # Executando atualizações concorrentes
    resultados = await asyncio.gather(*transacoes)

    # Verificando se as atualizações foram aplicadas corretamente
    assert len(resultados) == 2

    resposta_api_conta = client_api.get(
        "api/conta_bancarias?numero_da_conta=123",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "80.00"

    resposta_api_conta_2 = client_api.get(
        "api/conta_bancarias?numero_da_conta=456",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta_2.status_code == 200, resposta_api_conta_2.text
    assert resposta_api_conta_2.json()[0]["saldo"] == "10.00"

    resposta_api_conta_3 = client_api.get(
        "api/conta_bancarias?numero_da_conta=789",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta_3.status_code == 200, resposta_api_conta_3.text
    assert resposta_api_conta_3.json()[0]["saldo"] == "10.00"
