from business_contexts.utils.base_types import CPF


class TestClientAPI:
    """Testes de integração para a API de clientes."""

    def _auth_headers(self, mock_user_api) -> dict[str, str]:
        """Retorna headers de autenticação."""
        return {"Authorization": f"Bearer {mock_user_api.token}"}

    def test_register_client(self, client_api, mock_user_api) -> None:
        """Cadastro de cliente retorna 200 e dados corretos."""
        data = {"name": "João", "cpf": CPF.generate()}

        response = client_api.post(
            "api/cliente", json=data, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == data["name"]
        assert body["cpf"] == data["cpf"]
        assert "id" in body

    def test_register_duplicate_client_returns_409(
        self, client_api, mock_user_api, mock_client
    ) -> None:
        """Cadastro de cliente com CPF duplicado retorna 409."""
        data = {"name": "Outro", "cpf": str(mock_client.cpf)}

        response = client_api.post(
            "api/cliente", json=data, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 409

    def test_list_clients(self, client_api, mock_user_api, mock_client) -> None:
        """Listagem de clientes retorna ao menos um resultado."""
        response = client_api.get(
            "api/clientes", headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["id"] == str(mock_client.id)

    def test_query_by_cpf(self, client_api, mock_user_api, mock_client) -> None:
        """Consulta por CPF retorna o cliente correto."""
        response = client_api.get(
            f"api/clientes?cpf={mock_client.cpf}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()[0]["cpf"] == str(mock_client.cpf)

    def test_query_by_id(self, client_api, mock_user_api, mock_client) -> None:
        """Consulta por ID retorna o cliente correto."""
        response = client_api.get(
            f"api/clientes?id={mock_client.id}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()[0]["id"] == str(mock_client.id)

    def test_query_nonexistent_returns_404(self, client_api, mock_user_api) -> None:
        """Consulta de cliente inexistente retorna 404."""
        response = client_api.get(
            "api/clientes?cpf=00000000000",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 404

    def test_update_by_cpf(
        self, client_api, mock_user_api, mock_client, mock_client_gen
    ) -> None:
        """Atualização por CPF retorna dados atualizados."""
        updated = mock_client_gen
        updated["name"] = "Atualizado"

        response = client_api.put(
            f"api/cliente?cpf={mock_client.cpf}",
            json=updated,
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Atualizado"
        assert response.json()["id"] == str(mock_client.id)

    def test_update_by_id(
        self, client_api, mock_user_api, mock_client, mock_client_gen
    ) -> None:
        """Atualização por ID retorna dados atualizados."""
        updated = mock_client_gen
        updated["name"] = "Atualizado"

        response = client_api.put(
            f"api/cliente?id={mock_client.id}",
            json=updated,
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Atualizado"

    def test_delete_by_cpf(self, client_api, mock_user_api, mock_client) -> None:
        """Exclusão por CPF retorna 200."""
        response = client_api.delete(
            f"api/cliente?cpf={mock_client.cpf}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_delete_by_id(self, client_api, mock_user_api, mock_client) -> None:
        """Exclusão por ID retorna 200."""
        response = client_api.delete(
            f"api/cliente?id={mock_client.id}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_unauthenticated_returns_401(self, client_api) -> None:
        """Requisição sem token retorna 401."""
        response = client_api.get("api/clientes")

        assert response.status_code == 401
