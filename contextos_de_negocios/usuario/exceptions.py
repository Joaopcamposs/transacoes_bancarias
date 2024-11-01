from dataclasses import dataclass

from fastapi import status, HTTPException


@dataclass
class UsuarioNaoEncontrado(HTTPException):
    detail: str = "Usuario não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class UsuarioJaCadastrado(HTTPException):
    detail: str = "Email de Usuario já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class PermissaoFaltando(HTTPException):
    detail: str = "Esse usuário não tem permissão para executar essa ação."
    status_code: int = status.HTTP_403_FORBIDDEN


@dataclass
class ErroAoCadastrarUsuario(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarUsuario(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarUsuario(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
