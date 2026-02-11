from decimal import Decimal


class TestBankTransactionAPI:
    """Testes de integração para a API de transações bancárias."""

    def _auth_headers(self, mock_user_api) -> dict[str, str]:
        return {"Authorization": f"Bearer {mock_user_api.token}"}

    def test_deposit(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Depósito aumenta o saldo da conta."""
        mock_bank_account(account_number="500001", balance=Decimal("0.00"))

        response = client_api.post(
            "api/transacao_bancaria",
            json={"type": "deposit", "amount": 100.00, "account_number": "500001"},
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert response.json()["type"] == "deposit"
        assert response.json()["amount"] == "100.00"

        account = client_api.get(
            "api/conta_bancarias?account_number=500001",
            headers=self._auth_headers(mock_user_api),
        )
        assert account.json()[0]["balance"] == "100.00"

    def test_withdrawal(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Saque diminui o saldo da conta."""
        mock_bank_account(account_number="500002", balance=Decimal("100.00"))

        response = client_api.post(
            "api/transacao_bancaria",
            json={"type": "withdrawal", "amount": 40.00, "account_number": "500002"},
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

        account = client_api.get(
            "api/conta_bancarias?account_number=500002",
            headers=self._auth_headers(mock_user_api),
        )
        assert account.json()[0]["balance"] == "60.00"

    def test_withdrawal_insufficient_balance(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Saque com saldo insuficiente retorna 400."""
        mock_bank_account(account_number="500003", balance=Decimal("10.00"))

        response = client_api.post(
            "api/transacao_bancaria",
            json={"type": "withdrawal", "amount": 50.00, "account_number": "500003"},
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 400

    def test_transfer(self, client_api, mock_user_api, mock_bank_account) -> None:
        """Transferência movimenta saldo entre contas."""
        mock_bank_account(account_number="600001", balance=Decimal("100.00"))
        mock_bank_account(account_number="600002", balance=Decimal("0.00"))

        response = client_api.post(
            "api/transacao_bancaria",
            json={
                "type": "transfer",
                "amount": 30.00,
                "account_number": "600001",
                "destination_account_number": "600002",
            },
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200

        origin = client_api.get(
            "api/conta_bancarias?account_number=600001",
            headers=self._auth_headers(mock_user_api),
        )
        assert origin.json()[0]["balance"] == "70.00"

        destination = client_api.get(
            "api/conta_bancarias?account_number=600002",
            headers=self._auth_headers(mock_user_api),
        )
        assert destination.json()[0]["balance"] == "30.00"

    def test_transfer_insufficient_balance(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Transferência com saldo insuficiente retorna 400."""
        mock_bank_account(account_number="600003", balance=Decimal("5.00"))
        mock_bank_account(account_number="600004", balance=Decimal("0.00"))

        response = client_api.post(
            "api/transacao_bancaria",
            json={
                "type": "transfer",
                "amount": 50.00,
                "account_number": "600003",
                "destination_account_number": "600004",
            },
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 400

    def test_transfer_to_nonexistent_account(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Transferência para conta inexistente retorna 404."""
        mock_bank_account(account_number="600005", balance=Decimal("100.00"))

        response = client_api.post(
            "api/transacao_bancaria",
            json={
                "type": "transfer",
                "amount": 10.00,
                "account_number": "600005",
                "destination_account_number": "999999",
            },
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 404

    def test_list_transactions(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Listagem de transações retorna ao menos uma."""
        mock_bank_account(account_number="700001", balance=Decimal("0.00"))
        client_api.post(
            "api/transacao_bancaria",
            json={"type": "deposit", "amount": 10.00, "account_number": "700001"},
            headers=self._auth_headers(mock_user_api),
        )

        response = client_api.get(
            "api/transacao_bancarias",
            headers=self._auth_headers(mock_user_api),
        )

        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_unauthenticated_returns_401(self, client_api) -> None:
        """Requisição sem token retorna 401."""
        response = client_api.post(
            "api/transacao_bancaria",
            json={"type": "deposit", "amount": 10.00, "account_number": "123"},
        )

        assert response.status_code == 401


class TestConcurrency:
    """Testes de concorrência para transações bancárias."""

    def _auth_headers(self, mock_user_api) -> dict[str, str]:
        return {"Authorization": f"Bearer {mock_user_api.token}"}

    def _make_transaction(self, client_api, mock_user_api, **kwargs) -> dict:
        """Helper para executar uma transação bancária."""
        return client_api.post(
            "api/transacao_bancaria",
            json=kwargs,
            headers=self._auth_headers(mock_user_api),
        ).json()

    def test_sequential_deposit_and_withdrawal(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Depósito seguido de saque resulta no saldo correto."""
        mock_bank_account(account_number="800001", balance=Decimal("0.00"))

        self._make_transaction(
            client_api,
            mock_user_api,
            type="deposit",
            amount=50.00,
            account_number="800001",
        )
        self._make_transaction(
            client_api,
            mock_user_api,
            type="withdrawal",
            amount=30.00,
            account_number="800001",
        )

        account = client_api.get(
            "api/conta_bancarias?account_number=800001",
            headers=self._auth_headers(mock_user_api),
        )
        assert account.json()[0]["balance"] == "20.00"

    def test_sequential_deposit_and_transfer(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Depósito seguido de transferência resulta nos saldos corretos."""
        mock_bank_account(account_number="800002", balance=Decimal("0.00"))
        mock_bank_account(account_number="800003", balance=Decimal("0.00"))

        self._make_transaction(
            client_api,
            mock_user_api,
            type="deposit",
            amount=100.00,
            account_number="800002",
        )
        self._make_transaction(
            client_api,
            mock_user_api,
            type="transfer",
            amount=50.00,
            account_number="800002",
            destination_account_number="800003",
        )

        origin = client_api.get(
            "api/conta_bancarias?account_number=800002",
            headers=self._auth_headers(mock_user_api),
        )
        assert origin.json()[0]["balance"] == "50.00"

        dest = client_api.get(
            "api/conta_bancarias?account_number=800003",
            headers=self._auth_headers(mock_user_api),
        )
        assert dest.json()[0]["balance"] == "50.00"

    def test_multiple_transfers(
        self, client_api, mock_user_api, mock_bank_account
    ) -> None:
        """Múltiplas transferências entre contas resultam nos saldos corretos."""
        mock_bank_account(account_number="800004", balance=Decimal("100.00"))
        mock_bank_account(account_number="800005", balance=Decimal("0.00"))
        mock_bank_account(account_number="800006", balance=Decimal("0.00"))

        self._make_transaction(
            client_api,
            mock_user_api,
            type="transfer",
            amount=20.00,
            account_number="800004",
            destination_account_number="800005",
        )
        self._make_transaction(
            client_api,
            mock_user_api,
            type="transfer",
            amount=10.00,
            account_number="800005",
            destination_account_number="800006",
        )

        acc1 = client_api.get(
            "api/conta_bancarias?account_number=800004",
            headers=self._auth_headers(mock_user_api),
        )
        assert acc1.json()[0]["balance"] == "80.00"

        acc2 = client_api.get(
            "api/conta_bancarias?account_number=800005",
            headers=self._auth_headers(mock_user_api),
        )
        assert acc2.json()[0]["balance"] == "10.00"

        acc3 = client_api.get(
            "api/conta_bancarias?account_number=800006",
            headers=self._auth_headers(mock_user_api),
        )
        assert acc3.json()[0]["balance"] == "10.00"
