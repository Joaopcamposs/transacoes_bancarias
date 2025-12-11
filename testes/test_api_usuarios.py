def _criar_usuario_teste(client_api, token, dados=None):
    """Helper para criar usuário de teste via API."""
    from contextos_de_negocios.utils.tipos_basicos import CPF

    if dados is None:
        dados = {
            "nome": "Usuário Teste",
            "email": f"teste_{CPF.gerar()[:8]}@email.com",
            "senha": "1234",
            "adm": False,
            "ativo": True,
        }
    response = client_api.post(
        "api/usuario",
        json=dados,
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json(), dados


def test_cadastrar_usuario(client_api, mock_usuario_api, mock_usuario_gen):
    dados_usuario = mock_usuario_gen

    response = client_api.post(
        "api/usuario",
        json=dados_usuario,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    id_usuario = response.json()["id"]

    dados_esperados = {k: v for k, v in dados_usuario.items() if k != "senha"}
    assert response.json() == {
        "id": id_usuario,
        **dados_esperados,
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
    # Criar um usuário novo para ter ID válido
    usuario, _ = _criar_usuario_teste(client_api, mock_usuario_api.token)
    id_usuario = usuario["id"]

    response = client_api.get(
        f"api/usuarios?id={id_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_atualizar_usuario_por_email(client_api, mock_usuario_api):
    # Criar usuário novo para atualizar
    usuario, dados_originais = _criar_usuario_teste(client_api, mock_usuario_api.token)
    email_usuario = usuario["email"]

    usuario_atualizado = {
        "nome": "Teste Atualizado",
        "email": dados_originais["email"],
        "senha": "nova_senha",
        "adm": False,
        "ativo": False,
    }

    response = client_api.put(
        f"api/usuario?email={email_usuario}",
        json=usuario_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["nome"] == "Teste Atualizado"


def test_atualizar_usuario_por_id(client_api, mock_usuario_api):
    # Criar usuário novo para atualizar
    usuario, dados_originais = _criar_usuario_teste(client_api, mock_usuario_api.token)
    id_usuario = usuario["id"]

    usuario_atualizado = {
        "nome": "Teste Atualizado Por ID",
        "email": dados_originais["email"],
        "senha": "nova_senha",
        "adm": False,
        "ativo": False,
    }

    response = client_api.put(
        f"api/usuario?id={id_usuario}",
        json=usuario_atualizado,
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["nome"] == "Teste Atualizado Por ID"


def test_excluir_usuario_por_email(client_api, mock_usuario_api):
    # Criar usuário novo para excluir
    usuario, _ = _criar_usuario_teste(client_api, mock_usuario_api.token)
    email_usuario = usuario["email"]

    response = client_api.delete(
        f"api/usuario?email={email_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text


def test_excluir_usuario_por_id(client_api, mock_usuario_api):
    # Criar usuário novo para excluir
    usuario, _ = _criar_usuario_teste(client_api, mock_usuario_api.token)
    id_usuario = usuario["id"]

    response = client_api.delete(
        f"api/usuario?id={id_usuario}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert response.status_code == 200, response.text
