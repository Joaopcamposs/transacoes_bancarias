from decimal import Decimal
from uuid import uuid4

import pytest

from business_contexts.domain.aggregates.client import Client
from business_contexts.domain.aggregates.user import User
from business_contexts.domain.aggregates.bank_account import Account
from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.entities.bank_transaction import CreateBankTransaction
from business_contexts.domain.exceptions import InsufficientBalanceForTransaction
from business_contexts.domain.value_objects.bank_transaction import TransactionType
from business_contexts.utils.base_types import CPF


class TestClientAggregate:
    """Testes unitários para o agregado Client."""

    def test_create_client(self) -> None:
        """Verifica a criação de um cliente com dados válidos."""
        cpf = CPF(CPF.generate())
        client = Client.return_aggregate_for_creation(name="João", cpf=cpf)

        assert client.name == "João"
        assert str(client.cpf) == str(cpf)
        assert client.id is None

    def test_update_client(self) -> None:
        """Verifica a atualização dos dados do cliente."""
        cpf = CPF(CPF.generate())
        new_cpf = CPF(CPF.generate())
        client = Client(id=uuid4(), name="João", cpf=cpf)

        client.update(name="Maria", cpf=new_cpf)

        assert client.name == "Maria"
        assert str(client.cpf) == str(new_cpf)

    def test_to_dict(self) -> None:
        """Verifica a conversão do agregado para dicionário."""
        cpf = CPF(CPF.generate())
        uid = uuid4()
        client = Client(id=uid, name="João", cpf=cpf)
        data = client.to_dict()

        assert data["name"] == "João"
        assert data["id"] == str(uid)
        assert "cpf" in data


class TestUserAggregate:
    """Testes unitários para o agregado User."""

    def test_create_user_with_encryption(self) -> None:
        """Verifica a criação de usuário com criptografia de senha."""
        user = User.return_aggregate_for_creation(
            name="Admin",
            email="Admin@Email.COM",
            password="123456",
            is_admin=True,
            is_active=True,
            encrypt_password=True,
        )

        assert user.name == "Admin"
        assert user.email == "admin@email.com"
        assert user.password != "123456"
        assert user.is_admin is True
        assert user.is_active is True

    def test_create_user_without_encryption(self) -> None:
        """Verifica a criação de usuário sem criptografia."""
        user = User.return_aggregate_for_creation(
            name="Test",
            email="test@test.com",
            password="plain",
            is_admin=False,
            is_active=True,
            encrypt_password=False,
        )

        assert user.password == "plain"

    def test_verify_password(self) -> None:
        """Verifica a validação de senha do usuário."""
        user = User.return_aggregate_for_creation(
            name="Test",
            email="test@test.com",
            password="secret123",
            is_admin=False,
            is_active=True,
        )

        assert user.verify_password("secret123") is True
        assert user.verify_password("wrong") is False

    def test_update_user(self) -> None:
        """Verifica a atualização dos dados do usuário."""
        user = User(
            id=uuid4(),
            name="Old",
            email="old@test.com",
            password="pass",
            is_admin=False,
            is_active=True,
        )

        user.update(
            name="New",
            email="new@test.com",
            password="newpass",
            is_admin=True,
            is_active=False,
        )

        assert user.name == "New"
        assert user.email == "new@test.com"
        assert user.is_admin is True
        assert user.is_active is False


class TestBankAccountAggregate:
    """Testes unitários para o agregado Account."""

    def _make_account(self, balance: Decimal = Decimal("100.00")) -> Account:
        """Helper para criar uma conta para testes."""
        return Account(
            id=uuid4(),
            account_number="123456",
            balance=balance,
            client_cpf="12345678901",
        )

    def test_create_account(self) -> None:
        """Verifica a criação de uma conta bancária."""
        account = Account.return_aggregate_for_creation(
            account_number="123456",
            balance=Decimal("50.00"),
            client_cpf="12345678901",
        )

        assert account.account_number == "123456"
        assert account.balance == Decimal("50.00")
        assert account.id is None

    def test_deposit(self) -> None:
        """Verifica que depósito aumenta o saldo."""
        account = self._make_account(Decimal("100.00"))
        transaction = CreateBankTransaction(
            type=TransactionType.DEPOSIT,
            amount=Decimal("50.00"),
            account_number="123456",
        )

        result = account.new_transaction(transaction)

        assert account.balance == Decimal("150.00")
        assert result.type == TransactionType.DEPOSIT
        assert result.amount == Decimal("50.00")

    def test_withdrawal(self) -> None:
        """Verifica que saque diminui o saldo."""
        account = self._make_account(Decimal("100.00"))
        transaction = CreateBankTransaction(
            type=TransactionType.WITHDRAWAL,
            amount=Decimal("30.00"),
            account_number="123456",
        )

        result = account.new_transaction(transaction)

        assert account.balance == Decimal("70.00")
        assert result.type == TransactionType.WITHDRAWAL

    def test_withdrawal_insufficient_balance(self) -> None:
        """Verifica que saque com saldo insuficiente lança exceção."""
        account = self._make_account(Decimal("10.00"))
        transaction = CreateBankTransaction(
            type=TransactionType.WITHDRAWAL,
            amount=Decimal("50.00"),
            account_number="123456",
        )

        with pytest.raises(InsufficientBalanceForTransaction):
            account.new_transaction(transaction)

    def test_transfer(self) -> None:
        """Verifica que transferência diminui o saldo da conta de origem."""
        account = self._make_account(Decimal("100.00"))
        transaction = CreateBankTransaction(
            type=TransactionType.TRANSFER,
            amount=Decimal("40.00"),
            account_number="123456",
            destination_account_number="654321",
        )

        result = account.new_transaction(transaction)

        assert account.balance == Decimal("60.00")
        assert result.type == TransactionType.TRANSFER
        assert result.destination_account_number == "654321"

    def test_transfer_insufficient_balance(self) -> None:
        """Verifica que transferência com saldo insuficiente lança exceção."""
        account = self._make_account(Decimal("5.00"))
        transaction = CreateBankTransaction(
            type=TransactionType.TRANSFER,
            amount=Decimal("50.00"),
            account_number="123456",
            destination_account_number="654321",
        )

        with pytest.raises(InsufficientBalanceForTransaction):
            account.new_transaction(transaction)

    def test_negative_amount_raises(self) -> None:
        """Verifica que valor negativo lança exceção."""
        account = self._make_account()
        transaction = CreateBankTransaction(
            type=TransactionType.DEPOSIT,
            amount=Decimal("-10.00"),
            account_number="123456",
        )

        with pytest.raises(ValueError):
            account.new_transaction(transaction)


class TestTransactionAggregate:
    """Testes unitários para o agregado Transaction."""

    def test_create_transaction(self) -> None:
        """Verifica a criação de uma transação."""
        from business_contexts.domain.business_rules.bank_transaction import (
            get_local_time,
        )

        now = get_local_time()
        tx = Transaction.return_aggregate_for_creation(
            type=TransactionType.DEPOSIT,
            amount=Decimal("100.00"),
            date=now,
            account_number="123456",
        )

        assert tx.type == TransactionType.DEPOSIT
        assert tx.amount == Decimal("100.00")
        assert tx.account_number == "123456"
        assert tx.destination_account_number is None
        assert tx.id is None
