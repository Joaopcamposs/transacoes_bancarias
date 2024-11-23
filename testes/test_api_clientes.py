from contextos_de_negocios.utils.tipos_basicos import CPF


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


def test_listar_todos_clientes(client_api, mock_usuario_api, mock_cliente):
    response = client_api.get(
        "api/clientes",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()[0] == mock_cliente.to_dict()


def test_consultar_cliente_por_cpf(client_api, mock_usuario_api, mock_cliente):
    cpf_cliente = mock_cliente.cpf

    response = client_api.get(
        f"api/clientes?cpf={cpf_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()[0] == mock_cliente.to_dict()


def test_consultar_cliente_por_id(client_api, mock_usuario_api, mock_cliente):
    id_cliente = mock_cliente.id

    response = client_api.get(
        f"api/clientes?id={id_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()[0] == mock_cliente.to_dict()


def test_atualizar_cliente_por_cpf(
    client_api, mock_usuario_api, mock_cliente, mock_cliente_gen
):
    cpf_cliente, id_cliente = mock_cliente.cpf, mock_cliente.id

    cliente_atualizado = mock_cliente_gen
    cliente_atualizado["nome"] = "Teste Atualizado"

    response = client_api.put(
        f"api/cliente?cpf={cpf_cliente}",
        json=cliente_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(id_cliente),
        **cliente_atualizado,
    }


def test_atualizar_cliente_por_id(
    client_api, mock_usuario_api, mock_cliente, mock_cliente_gen
):
    id_cliente = mock_cliente.id

    cliente_atualizado = mock_cliente_gen
    cliente_atualizado["nome"] = "Teste Atualizado"

    response = client_api.put(
        f"api/cliente?id={id_cliente}",
        json=cliente_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(id_cliente),
        **cliente_atualizado,
    }


def test_excluir_cliente_por_cpf(client_api, mock_usuario_api, mock_cliente):
    cpf_cliente = mock_cliente.cpf

    response = client_api.delete(
        f"api/cliente?cpf={cpf_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_excluir_cliente_por_id(client_api, mock_usuario_api, mock_cliente):
    id_cliente = mock_cliente.id

    response = client_api.delete(
        f"api/cliente?id={id_cliente}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
