from business_contexts.domain.value_objects.bank_transaction import TransactionType
from libs.ddd.adapters.viewers import Filters


class TestTransactionType:
    """Testes unitários para o enum TransactionType."""

    def test_values(self) -> None:
        """Verifica os valores do enum TransactionType."""
        assert TransactionType.DEPOSIT.value == "deposit"
        assert TransactionType.WITHDRAWAL.value == "withdrawal"
        assert TransactionType.TRANSFER.value == "transfer"

    def test_members(self) -> None:
        """Verifica que existem exatamente 3 tipos de transação."""
        assert len(TransactionType) == 3


class TestFilters:
    """Testes unitários para a classe Filters."""

    def test_filters_removes_none(self) -> None:
        """Verifica que Filters remove valores None."""
        filters = Filters({"name": "João", "email": None, "age": 30})
        assert dict(filters) == {"name": "João", "age": 30}

    def test_filters_empty(self) -> None:
        """Verifica que filtros vazios resultam em dict vazio."""
        filters = Filters({})
        assert dict(filters) == {}

    def test_filters_all_none(self) -> None:
        """Verifica que filtros todos None resultam em dict vazio."""
        filters = Filters({"a": None, "b": None})
        assert dict(filters) == {}

    def test_filters_str(self) -> None:
        """Verifica a representação em string dos filtros."""
        filters = Filters({"name": "Test"})
        assert str(filters) == "{'name': 'Test'}"
