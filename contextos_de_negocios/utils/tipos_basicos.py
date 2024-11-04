from enum import Enum
from random import randint

from validate_docbr import CPF as ValidadorDeCPF


class TipoOperacao(Enum):
    INSERCAO = "insercao"
    ATUALIZACAO = "atualizacao"
    REMOCAO = "remocao"


class CPF(ValidadorDeCPF):
    def __init__(self, cpf: str = ""):
        self.cpf = self.somente_digitos(cpf)

    def validar(self) -> None:
        if not self.validate():
            raise ValueError("CPF inválido")

    @staticmethod
    def somente_digitos(cpf: str) -> str:
        return "".join([char for char in cpf if char.isdigit()])

    @staticmethod
    def gerar() -> str:
        cpf_gerado = ValidadorDeCPF().generate()
        return str(cpf_gerado)


class NumeroDaConta(str):
    def __post_init__(self, numero_da_conta: str = "") -> None:
        numero_da_conta = self.somente_digitos(numero_da_conta)
        self.validar(numero_da_conta)

    def __new__(cls, numero_da_conta: str) -> str:
        numero_da_conta = cls.somente_digitos(numero_da_conta)
        cls.validar(numero_da_conta)
        return numero_da_conta

    @classmethod
    def validar(cls, numero_da_conta: str) -> None:
        if numero_da_conta is None or not cls.validar_numero_da_conta(numero_da_conta):
            raise ValueError(
                "Número da conta inválido. Necessário ser pelo menos três dígitos"
            )

    @staticmethod
    def somente_digitos(numero_da_conta: str) -> str:
        return "".join([char for char in numero_da_conta if char.isdigit()])

    @staticmethod
    def validar_numero_da_conta(numero_da_conta: str) -> bool:
        return len(numero_da_conta) >= 3 and numero_da_conta.isdigit()

    @staticmethod
    def gerar_numero_da_conta() -> str:
        return str(randint(100000, 999999))
