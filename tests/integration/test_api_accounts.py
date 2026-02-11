from decimal import Decimal


class TestBankAccountAPI:
    """Testes de integração para a API de contas bancárias."""

    def _auth_headers(self, mock_user_api) -> dict[str, str]:
        return {"Authorization": f"Bearer {mock_user_api.token}"}

    def test_register_account(
        self, client_api, mock_user_api, mock_client, mock_bank_account_gen
    ) -> None:
        """Cadastro de conta bancária retorna 200."""
        data = mock_bank_account_gen
        data["client_cpf"] = mock_client.cpf

        response = client_api.post(
            "api/conta_bancaria", json=data, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 200
        body = response.json()
        assert body["account_number"] == data["account_number"]
        assert "id" in body

    def test_register_duplicate_account_returns_409(
        self, client_api, mock_user_api, mock_client
    ) -> None:
        """Cadastro de conta com número duplicado retorna 409."""
        data = {
            "account_number": "999888",
            "balance": "0.00",
            "client_cpf": mock_client.cpf,
        }

        client_api.post(
            "api/conta_bancaria", json=data, headers=self._auth_headers(mock_user_api)
        )
        response = client_api.post(
            "api/conta_bancaria", json=data, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 409

    def test_register_account_nonexistent_client_returns_404(
        self, client_api, mock_user_api
    ) -> None:
        """Cadastro de conta para cliente inexistente retorna 404."""
        data = {
            "account_number": "111222",
            "balance": "0.00",
            "client_cpf": "99999999999",
        }

        response = client_api.post(
            "api/conta_bancaria", json=data, headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 404

    def test_list_accounts(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Listagem de contas retorna ao menos uma conta."""
        mock_bank_account(account_number="100001", balance=Decimal("50.00"))

        response = client_api.get(
            "api/conta_bancarias", headers=self._auth_headers(mock_user_api)
        )

        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_query_by_account_number(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Consulta por número da conta retorna a conta correta."""
        account = mock_bank_account(account_number="200001", balance=Decimal("100.00"))

        response = client_api.get(
            f"api/conta_bancarias?account_number={account.account_number}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()[0]["account_number"] == account.account_number

    def test_query_by_id(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Consulta por ID retorna a conta correta."""
        account = mock_bank_account(account_number="200002", balance=Decimal("100.00"))

        response = client_api.get(
            f"api/conta_bancarias?id={account.id}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()[0]["id"] == account.id

    def test_list_with_transactions(
        self, client_api, mock_user_api, mock_bank_account, mock_bank_transaction
    ) -> None:
        """Consulta com transações retorna lista de transações."""
        mock_bank_account(account_number="200003", balance=Decimal("100.00"))
        mock_bank_transaction(account_number="200003", amount=50.00)

        response = client_api.get(
            "api/conta_bancarias?account_number=200003&list_transactions=true",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert len(response.json()[0].get("transactions", [])) >= 1

    def test_update_by_account_number(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Atualização por número da conta retorna dados atualizados."""
        account = mock_bank_account(account_number="300001", balance=Decimal("0.00"))

        updated = {"account_number": "300002", "client_cpf": account.client_cpf}
        response = client_api.put(
            "api/conta_bancaria?account_number=300001",
            json=updated,
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()["account_number"] == "300002"

    def test_update_by_id(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Atualização por ID retorna dados atualizados."""
        account = mock_bank_account(account_number="300003", balance=Decimal("0.00"))

        updated = {"account_number": "300004", "client_cpf": account.client_cpf}
        response = client_api.put(
            f"api/conta_bancaria?id={account.id}",
            json=updated,
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_delete_by_account_number(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Exclusão por número da conta retorna 200."""
        mock_bank_account(account_number="400001", balance=Decimal("0.00"))

        response = client_api.delete(
            "api/conta_bancaria?account_number=400001",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_delete_by_id(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Exclusão por ID retorna 200."""
        account = mock_bank_account(account_number="400002", balance=Decimal("0.00"))

        response = client_api.delete(
            f"api/conta_bancaria?id={account.id}",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

    def test_unauthenticated_returns_401(self, client_api) -> None:
        """Requisição sem token retorna 401."""
        response = client_api.get("api/conta_bancarias")

        assert response.status_code == 401
