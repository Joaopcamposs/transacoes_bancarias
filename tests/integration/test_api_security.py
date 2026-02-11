class TestSecurityAPI:
    """Testes de integração para a API de autenticação e segurança."""

    def test_login_success(self, client_api, mock_user_api) -> None:
        """Login com credenciais válidas retorna token."""
        response = client_api.post(
            "api/token",
            data={"username": mock_user_api.email, "password": mock_user_api.password},
        )

        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_wrong_password(self, client_api, mock_user_api) -> None:
        """Login com senha incorreta retorna erro."""
        response = client_api.post(
            "api/token",
            data={"username": mock_user_api.email, "password": "wrong_password"},
        )

        assert response.status_code == 500

    def test_login_nonexistent_user(self, client_api) -> None:
        """Login com email inexistente retorna erro."""
        response = client_api.post(
            "api/token",
            data={"username": "nobody@test.com", "password": "1234"},
        )

        assert response.status_code == 500

    def test_get_current_user(self, client_api, mock_user_api) -> None:
        """Rota /usuario/me retorna dados do usuário autenticado."""
        response = client_api.get(
            "api/usuario/me",
            headers={"Authorization": f"Bearer {mock_user_api.token}"},
        )

        assert response.status_code == 200
        assert response.json()["email"] == mock_user_api.email

    def test_get_current_user_invalid_token(self, client_api) -> None:
        """Rota /usuario/me com token inválido retorna 401."""
        response = client_api.get(
            "api/usuario/me",
            headers={"Authorization": "Bearer invalid_token_here"},
        )

        assert response.status_code == 401

    def test_root_route(self, client_api) -> None:
        """Rota raiz retorna Hello World."""
        response = client_api.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_test_route(self, client_api) -> None:
        """Rota /test retorna OK."""
        response = client_api.get("/test")

        assert response.status_code == 200
