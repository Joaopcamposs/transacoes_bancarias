def test_cadastrar_usuario(
    client_api,
    mock_usuario_api,
    mock_usuario_gen,
):
    dados_usuario = mock_usuario_gen

    response = client_api.post(
        "api/usuario",
        json=dados_usuario,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    id_usuario = response.json()["id"]

    dados_usuario.pop("senha")
    assert response.json() == {
        "id": id_usuario,
        **dados_usuario,
    }


def test_listar_todos_usuarios(client_api, mock_usuario_api):
    response = client_api.get(
        "api/usuarios",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_consultar_usuario_por_email(client_api, mock_usuario_api):
    email_usuario = mock_usuario_api.email

    response = client_api.get(
        f"api/usuarios?email={email_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_consultar_usuario_por_id(client_api, mock_usuario_api):
    id_usuario = mock_usuario_api.id

    response = client_api.get(
        f"api/usuarios?id={id_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_atualizar_usuario_por_email(client_api, mock_usuario_api, mock_usuario_gen):
    email_usuario, id_usuario = mock_usuario_api.email, mock_usuario_api.id

    usuario_atualizado = mock_usuario_gen
    usuario_atualizado["nome"] = "Teste Atualizado"
    usuario_atualizado["ativo"] = False

    response = client_api.put(
        f"api/usuario?email={email_usuario}",
        json=usuario_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    usuario_atualizado.pop("senha")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(id_usuario),
        **usuario_atualizado,
    }


def test_atualizar_usuario_por_id(client_api, mock_usuario_api, mock_usuario_gen):
    id_usuario = mock_usuario_api.id

    usuario_atualizado = mock_usuario_gen
    usuario_atualizado["nome"] = "Teste Atualizado"
    usuario_atualizado["ativo"] = False

    response = client_api.put(
        f"api/usuario?id={id_usuario}",
        json=usuario_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    usuario_atualizado.pop("senha")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(id_usuario),
        **usuario_atualizado,
    }


def test_excluir_usuario_por_email(client_api, mock_usuario_api):
    email_usuario = mock_usuario_api.email

    response = client_api.delete(
        f"api/usuario?email={email_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_excluir_usuario_por_id(client_api, mock_usuario_api):
    id_usuario = mock_usuario_api.id

    response = client_api.delete(
        f"api/usuario?id={id_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
