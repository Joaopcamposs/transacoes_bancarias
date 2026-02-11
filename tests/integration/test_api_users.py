class TestUserAPI:
    """Testes de integração para a API de usuários."""

    def _auth_headers(self, mock_user_api) -> dict[str, str]:
        return {"Authorization": f"Bearer {mock_user_api.token}"}

    def _create_test_user(self, client_api, mock_user_api) -> dict:
        """Cria um usuário de teste auxiliar (não-admin) e retorna os dados."""
        data = {
            "name": "Teste User",
            "email": "teste@email.com",
            "password": "senha123",
            "is_admin": False,
            "is_active": True,
        }
        resp = client_api.post(
            "api/usuario", json=data, headers=self._auth_headers(mock_user_api)
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        body["password"] = data["password"]
        return body

    def test_register_user(self, client_api, mock_user_api, mock_user_gen) -> None:
        """Cadastro de usuário retorna 200 e dados corretos."""
        response = client_api.post(
            "api/usuario", json=mock_user_gen, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == mock_user_gen["name"]
        assert body["email"] == mock_user_gen["email"]
        assert "password" not in body
        assert "id" in body

    def test_register_duplicate_user_returns_409(
        self, client_api, mock_user_api
    ) -> None:
        """Cadastro de usuário com email duplicado retorna 409."""
        data = {
            "name": "Dup",
            "email": mock_user_api.email,
            "password": "1234",
            "is_admin": False,
            "is_active": True,
        }

        response = client_api.post(
            "api/usuario", json=data, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 409

    def test_list_users(self, client_api, mock_user_api) -> None:
        """Listagem de usuários retorna ao menos o admin."""
        response = client_api.get(
            "api/usuarios", headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_query_by_email(self, client_api, mock_user_api) -> None:
        """Consulta por email retorna o usuário correto."""
        response = client_api.get(
            f"api/usuarios?email={mock_user_api.email}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()[0]["email"] == mock_user_api.email

    def test_query_by_id(self, client_api, mock_user_api) -> None:
        """Consulta por ID retorna o usuário correto."""
        response = client_api.get(
            f"api/usuarios?id={mock_user_api.id}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()[0]["id"] == str(mock_user_api.id)

    def test_update_by_email(self, client_api, mock_user_api) -> None:
        """Atualização de usuário auxiliar por email retorna dados atualizados."""
        user = self._create_test_user(client_api, mock_user_api)

        updated = {
            "name": "Atualizado",
            "email": user["email"],
            "password": user["password"],
            "is_admin": False,
            "is_active": True,
        }
        response = client_api.put(
            f"api/usuario?email={user['email']}",
            json=updated,
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Atualizado"

    def test_update_by_id(self, client_api, mock_user_api) -> None:
        """Atualização de usuário auxiliar por ID retorna dados atualizados."""
        user = self._create_test_user(client_api, mock_user_api)

        updated = {
            "name": "Atualizado Por ID",
            "email": user["email"],
            "password": user["password"],
            "is_admin": False,
            "is_active": True,
        }
        response = client_api.put(
            f"api/usuario?id={user['id']}",
            json=updated,
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Atualizado Por ID"

    def test_delete_by_email(self, client_api, mock_user_api) -> None:
        """Exclusão de usuário auxiliar por email retorna 200."""
        user = self._create_test_user(client_api, mock_user_api)

        response = client_api.delete(
            f"api/usuario?email={user['email']}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_delete_by_id(self, client_api, mock_user_api) -> None:
        """Exclusão de usuário auxiliar por ID retorna 200."""
        user = self._create_test_user(client_api, mock_user_api)

        response = client_api.delete(
            f"api/usuario?id={user['id']}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_unauthenticated_returns_401(self, client_api) -> None:
        """Requisição sem token retorna 401."""
        response = client_api.get("api/usuarios")

        assert response.status_code == 401
