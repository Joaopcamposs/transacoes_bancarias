from random import randint
from testes.conftest import criar_cliente_teste


def _gerar_numero_conta():
    """Gera número de conta único para evitar conflitos."""
    return str(randint(1000000, 9999999))


def test_cadastrar_conta(client_api, mock_usuario_api):
    cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    dados_conta = {
        "numero_da_conta": _gerar_numero_conta(),
        "saldo": "100.00",
        "cpf_cliente": cliente.cpf,
    }

    response = client_api.post(
        "api/conta_bancaria",
        json=dados_conta,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_listar_todas_contas_bancarias(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    mock_conta_bancaria(saldo="100.00")

    response = client_api.get(
        "api/conta_bancarias",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_consultar_conta_bancaria_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="100.00")
    numero_da_conta = conta["numero_da_conta"]

    response = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero_da_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_consultar_conta_bancaria_e_transacoes_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria, mock_transacao_bancaria
):
    conta = mock_conta_bancaria(saldo="1000.00")
    mock_transacao_bancaria(
        tipo="deposito", valor="100.00", numero_da_conta=conta["numero_da_conta"]
    )
    numero_da_conta = conta["numero_da_conta"]

    response = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero_da_conta}&listar_transacoes=true",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_consultar_conta_bancaria_por_id(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="100.00")
    id_conta = conta["id"]

    response = client_api.get(
        f"api/conta_bancarias?id={id_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_atualizar_conta_bancaria_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="0.00")
    numero_da_conta = conta["numero_da_conta"]

    conta_atualizada = {
        "numero_da_conta": _gerar_numero_conta(),
        "saldo": "0.00",
        "cpf_cliente": conta["cpf_cliente"],
    }

    response = client_api.put(
        f"api/conta_bancaria?numero_da_conta={numero_da_conta}",
        json=conta_atualizada,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_atualizar_conta_bancaria_por_id(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="0.00")
    id_conta = conta["id"]

    conta_atualizada = {
        "numero_da_conta": _gerar_numero_conta(),
        "saldo": "0.00",
        "cpf_cliente": conta["cpf_cliente"],
    }

    response = client_api.put(
        f"api/conta_bancaria?id={id_conta}",
        json=conta_atualizada,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_excluir_conta_bancaria_por_numero_da_conta(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="100.00")
    numero_da_conta = conta["numero_da_conta"]

    response = client_api.delete(
        f"api/conta_bancaria?numero_da_conta={numero_da_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_excluir_conta_bancaria_por_id(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="100.00")
    id_conta = conta["id"]

    response = client_api.delete(
        f"api/conta_bancaria?id={id_conta}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
