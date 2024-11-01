from dataclasses import dataclass

from fastapi import HTTPException, status


@dataclass
class ContaBancariaNaoEncontrado(HTTPException):
    detail: str = "numero da ContaBancaria não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ContaBancariaJaCadastrado(HTTPException):
    detail: str = "numero da ContaBancaria já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErroAoCadastrarContaBancaria(HTTPException):
    detail: str = "Erro ao cadastrar conta bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarContaBancaria(HTTPException):
    detail: str = "Erro ao atualizar conta bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarContaBancaria(HTTPException):
    detail: str = "Erro ao deletar conta bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
