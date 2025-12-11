from contextos_de_negocios.utils.tipos_basicos import CPF
from testes.conftest import criar_cliente_teste


def test_cadastrar_cliente(client_api, mock_usuario_api):
    dados_cliente = {"nome": "João", "cpf": CPF.gerar()}

    response = client_api.post(
        "api/cliente",
        json=dados_cliente,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    id_cliente = response.json()["id"]
    assert response.json() == {
        "id": id_cliente,
        **dados_cliente,
    }


def test_listar_todos_clientes(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)

    response = client_api.get(
        "api/clientes",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    clientes = response.json()
    assert any(c["id"] == str(mock_cliente.id) for c in clientes)


def test_consultar_cliente_por_cpf(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    cpf_cliente = mock_cliente.cpf

    response = client_api.get(
        f"api/clientes?cpf={cpf_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()[0]["cpf"] == cpf_cliente


def test_consultar_cliente_por_id(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    id_cliente = mock_cliente.id

    response = client_api.get(
        f"api/clientes?id={id_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()[0]["id"] == str(id_cliente)


def test_atualizar_cliente_por_cpf(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    cpf_cliente = mock_cliente.cpf

    cliente_atualizado = {"nome": "Teste Atualizado", "cpf": CPF.gerar()}

    response = client_api.put(
        f"api/cliente?cpf={cpf_cliente}",
        json=cliente_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["nome"] == "Teste Atualizado"


def test_atualizar_cliente_por_id(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    id_cliente = mock_cliente.id

    cliente_atualizado = {"nome": "Teste Atualizado", "cpf": CPF.gerar()}

    response = client_api.put(
        f"api/cliente?id={id_cliente}",
        json=cliente_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["nome"] == "Teste Atualizado"


def test_excluir_cliente_por_cpf(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    cpf_cliente = mock_cliente.cpf

    response = client_api.delete(
        f"api/cliente?cpf={cpf_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_excluir_cliente_por_id(client_api, mock_usuario_api):
    mock_cliente = criar_cliente_teste(client_api, mock_usuario_api.token)
    id_cliente = mock_cliente.id

    response = client_api.delete(
        f"api/cliente?id={id_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
