from dataclasses import dataclass

from fastapi import status, HTTPException


# --- Client Exceptions ---


@dataclass
class ClientNotFound(HTTPException):
    """Exceção lançada quando o cliente não é encontrado."""

    detail: str = "Cliente não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ClientAlreadyRegistered(HTTPException):
    """Exceção lançada quando já existe um cliente com o mesmo CPF."""

    detail: str = "Email de Cliente já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErrorRegisteringClient(HTTPException):
    """Exceção lançada quando ocorre erro ao cadastrar cliente."""

    detail: str = "Erro ao cadastrar cliente."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorUpdatingClient(HTTPException):
    """Exceção lançada quando ocorre erro ao atualizar cliente."""

    detail: str = "Erro ao atualizar cliente."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorDeletingClient(HTTPException):
    """Exceção lançada quando ocorre erro ao deletar cliente."""

    detail: str = "Erro ao deletar cliente."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


# --- Bank Account Exceptions ---


@dataclass
class BankAccountNotFound(HTTPException):
    """Exceção lançada quando a conta bancária não é encontrada."""

    detail: str = "Conta bancária não encontrada"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class BankAccountAlreadyRegistered(HTTPException):
    """Exceção lançada quando já existe uma conta com o mesmo número."""

    detail: str = "Número da conta bancária já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErrorRegisteringBankAccount(HTTPException):
    """Exceção lançada quando ocorre erro ao cadastrar conta bancária."""

    detail: str = "Erro ao cadastrar conta bancária."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorUpdatingBankAccount(HTTPException):
    """Exceção lançada quando ocorre erro ao atualizar conta bancária."""

    detail: str = "Erro ao atualizar conta bancária."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorDeletingBankAccount(HTTPException):
    """Exceção lançada quando ocorre erro ao deletar conta bancária."""

    detail: str = "Erro ao deletar conta bancária."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class InsufficientBalanceForTransaction(HTTPException):
    """Exceção lançada quando o saldo é insuficiente para realizar a transação."""

    detail: str = "Saldo insuficiente para realizar a transação."
    status_code: int = status.HTTP_400_BAD_REQUEST


# --- User Exceptions ---


@dataclass
class UserNotFound(HTTPException):
    """Exceção lançada quando o usuário não é encontrado."""

    detail: str = "Usuário não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class UserAlreadyRegistered(HTTPException):
    """Exceção lançada quando já existe um usuário com o mesmo email."""

    detail: str = "Email de usuário já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class MissingPermission(HTTPException):
    """Exceção lançada quando o usuário não tem permissão para a ação."""

    detail: str = "Esse usuário não tem permissão para executar essa ação."
    status_code: int = status.HTTP_403_FORBIDDEN


@dataclass
class ErrorRegisteringUser(HTTPException):
    """Exceção lançada quando ocorre erro ao cadastrar usuário."""

    detail: str = "Erro ao cadastrar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorUpdatingUser(HTTPException):
    """Exceção lançada quando ocorre erro ao atualizar usuário."""

    detail: str = "Erro ao atualizar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorDeletingUser(HTTPException):
    """Exceção lançada quando ocorre erro ao deletar usuário."""

    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


# --- Bank Transaction Exceptions ---


@dataclass
class BankTransactionNotFound(HTTPException):
    """Exceção lançada quando a transação bancária não é encontrada."""

    detail: str = "Transação bancária não encontrada"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class BankTransactionAlreadyRegistered(HTTPException):
    """Exceção lançada quando a transação bancária já existe."""

    detail: str = "Transação bancária já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErrorRegisteringBankTransaction(HTTPException):
    """Exceção lançada quando ocorre erro ao cadastrar transação bancária."""

    detail: str = "Erro ao cadastrar transação bancária."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorUpdatingBankTransaction(HTTPException):
    """Exceção lançada quando ocorre erro ao atualizar transação bancária."""

    detail: str = "Erro ao atualizar transação bancária."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErrorDeletingBankTransaction(HTTPException):
    """Exceção lançada quando ocorre erro ao deletar transação bancária."""

    detail: str = "Erro ao deletar transação bancária."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class NegativeTransactionAmount(HTTPException):
    """Exceção lançada quando o valor da transação é negativo."""

    detail: str = "O valor da transação não pode ser negativo."
    status_code: int = status.HTTP_400_BAD_REQUEST


# --- Security Exceptions ---


@dataclass
class ErrorGeneratingToken(HTTPException):
    """Exceção lançada quando ocorre erro ao gerar o token de autenticação."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Erro ao gerar token."


@dataclass
class CouldNotValidateCredentials(HTTPException):
    """Exceção lançada quando não é possível validar as credenciais."""

    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Não foi possível validar as credenciais"


@dataclass
class IncorrectCredentials(HTTPException):
    """Exceção lançada quando email ou senha estão incorretos."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Email ou senha incorretos"


@dataclass
class ExpiredLogin(HTTPException):
    """Exceção lançada quando o login está expirado."""

    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Login expirado. Logue novamente"
