from decimal import Decimal

import pytest


def test_cadastrar_conta(
    client_api,
    mock_usuario_api,
    mock_cliente,
    mock_conta_bancaria_gen,
):
    dados_conta = mock_conta_bancaria_gen
    dados_conta["cpf_cliente"] = mock_cliente.cpf

    response = client_api.post(
        "api/conta_bancaria",
        json=dados_conta,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    id_conta = response.json()["id"]

    assert response.json() == {
        "id": id_conta,
        **dados_conta,
    }


@pytest.mark.asyncio
async def test_listar_todas_contas_bancarias(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))

    response = client_api.get(
        "api/conta_bancarias",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_consultar_conta_bancaria_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))
    numero_da_conta = conta.numero_da_conta

    response = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero_da_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_consultar_conta_bancaria_por_id(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))
    id_conta = conta.id

    response = client_api.get(
        f"api/conta_bancarias?id={id_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_atualizar_conta_bancaria_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria, mock_conta_bancaria_gen
):
    conta = await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(0.00))
    email_usuario, id_conta = conta.numero_da_conta, conta.id

    conta_atualizada = mock_conta_bancaria_gen
    conta_atualizada["cpf_cliente"] = conta.cpf_cliente
    conta_atualizada["numero_da_conta"] = "45678"

    response = client_api.put(
        f"api/conta_bancaria?numero_da_conta={email_usuario}",
        json=conta_atualizada,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(id_conta),
        **conta_atualizada,
    }


@pytest.mark.asyncio
async def test_atualizar_conta_bancaria_por_id(
    client_api,
    mock_usuario_api,
    mock_usuario_gen,
    mock_conta_bancaria,
    mock_conta_bancaria_gen,
):
    conta = await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(0.00))
    id_conta = conta.id

    conta_atualizada = mock_conta_bancaria_gen
    conta_atualizada["cpf_cliente"] = conta.cpf_cliente
    conta_atualizada["numero_da_conta"] = "45678"

    response = client_api.put(
        f"api/conta_bancaria?id={id_conta}",
        json=conta_atualizada,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(id_conta),
        **conta_atualizada,
    }


@pytest.mark.asyncio
async def test_excluir_conta_bancaria_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))
    numero_da_conta = conta.numero_da_conta

    response = client_api.delete(
        f"api/conta_bancaria?numero_da_conta={numero_da_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_excluir_conta_bancaria_por_id(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = await mock_conta_bancaria(numero_da_conta="123", saldo=Decimal(100.00))
    id_conta = conta.id

    response = client_api.delete(
        f"api/conta_bancaria?id={id_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
