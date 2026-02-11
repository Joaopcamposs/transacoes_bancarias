import pytest

from business_contexts.utils.base_types import CPF, AccountNumber, OperationType


class TestCPF:
    """Testes unitários para o tipo de valor CPF."""

    def test_valid_cpf(self) -> None:
        """Verifica que um CPF válido é aceito."""
        valid_cpf = CPF.generate()
        cpf = CPF(valid_cpf)
        assert len(str(cpf)) == 11

    def test_invalid_cpf_raises(self) -> None:
        """Verifica que um CPF inválido lança ValueError."""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("00000000000")

    def test_cpf_strips_non_digits(self) -> None:
        """Verifica que caracteres não numéricos são removidos."""
        valid_cpf = CPF.generate()
        formatted = f"{valid_cpf[:3]}.{valid_cpf[3:6]}.{valid_cpf[6:9]}-{valid_cpf[9:]}"
        cpf = CPF(formatted)
        assert str(cpf) == valid_cpf

    def test_generate_produces_valid_cpf(self) -> None:
        """Verifica que CPFs gerados são válidos."""
        for _ in range(5):
            generated = CPF.generate()
            cpf = CPF(generated)
            assert len(str(cpf)) == 11


class TestAccountNumber:
    """Testes unitários para o tipo de valor AccountNumber."""

    def test_valid_account_number(self) -> None:
        """Verifica que um número de conta válido é aceito."""
        number = AccountNumber("123456")
        assert number == "123456"

    def test_short_account_number_raises(self) -> None:
        """Verifica que número de conta com menos de 3 dígitos lança ValueError."""
        with pytest.raises(ValueError):
            AccountNumber("12")

    def test_non_digit_account_number_raises(self) -> None:
        """Verifica que número de conta com letras lança ValueError."""
        with pytest.raises(ValueError):
            AccountNumber("abc")

    def test_generate_account_number(self) -> None:
        """Verifica que número de conta gerado tem 6 dígitos."""
        number = AccountNumber.generate_account_number()
        assert len(number) == 6
        assert number.isdigit()


class TestOperationType:
    """Testes unitários para o enum OperationType."""

    def test_values(self) -> None:
        """Verifica os valores do enum OperationType."""
        assert OperationType.INSERT.value == "insert"
        assert OperationType.UPDATE.value == "update"
        assert OperationType.DELETE.value == "delete"
