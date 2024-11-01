from dataclasses import dataclass

from fastapi import status, HTTPException


@dataclass
class ClienteNaoEncontrado(HTTPException):
    detail: str = "Cliente não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ClienteJaCadastrado(HTTPException):
    detail: str = "Email de Cliente já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErroAoCadastrarCliente(HTTPException):
    detail: str = "Erro ao cadastrar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarCliente(HTTPException):
    detail: str = "Erro ao atualizar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarCliente(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
