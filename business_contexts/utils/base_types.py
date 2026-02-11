from enum import Enum
from random import randint

from validate_docbr import CPF as CPFValidator


class OperationType(Enum):
    """Tipos de operações disponíveis no repositório de domínio."""

    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"


class CPF(str):
    """Tipo de valor que representa e valida um CPF brasileiro."""

    def __init__(self, cpf: str = "") -> None:
        """Inicializa o CPF, extraindo apenas dígitos e validando."""
        self.cpf: str = self.only_digits(cpf)
        self.validate()

    def validate(self) -> None:
        """Valida o CPF utilizando a biblioteca validate-docbr."""
        if not CPFValidator().validate(self.cpf):
            raise ValueError("CPF inválido")

    @staticmethod
    def only_digits(cpf: str) -> str:
        """Retorna apenas os dígitos numéricos do CPF."""
        return "".join([char for char in cpf if char.isdigit()])

    @staticmethod
    def generate() -> str:
        """Gera um CPF válido aleatoriamente."""
        generated_cpf: str = CPFValidator().generate()
        return str(generated_cpf)

    def __str__(self) -> str:
        """Retorna a representação em string do CPF (apenas dígitos)."""
        return self.cpf


class AccountNumber(str):
    """Tipo de valor que representa e valida um número de conta bancária."""

    def __post_init__(self, account_number: str = "") -> None:
        """Pós-inicialização para validação do número da conta."""
        account_number = self.only_digits(account_number)
        self.validate(account_number)

    def __new__(cls, account_number: str) -> str:
        """Cria uma nova instância de AccountNumber, validando o número."""
        account_number = cls.only_digits(account_number)
        cls.validate(account_number)
        return account_number

    @classmethod
    def validate(cls, account_number: str) -> None:
        """Valida se o número da conta possui pelo menos três dígitos numéricos."""
        if account_number is None or not cls.validate_account_number(account_number):
            raise ValueError(
                "Número da conta inválido. Necessário ser pelo menos três dígitos"
            )

    @staticmethod
    def only_digits(account_number: str) -> str:
        """Retorna apenas os dígitos numéricos do número da conta."""
        return "".join([char for char in account_number if char.isdigit()])

    @staticmethod
    def validate_account_number(account_number: str) -> bool:
        """Verifica se o número da conta é composto por pelo menos 3 dígitos."""
        return len(account_number) >= 3 and account_number.isdigit()

    @staticmethod
    def generate_account_number() -> str:
        """Gera um número de conta aleatório com 6 dígitos."""
        return str(randint(100000, 999999))
