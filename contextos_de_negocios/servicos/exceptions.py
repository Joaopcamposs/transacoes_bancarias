from dataclasses import dataclass, field
from fastapi import status, HTTPException


@dataclass
class NaoFoiPossivelValidarAsCredenciais(HTTPException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Não foi possível validar as credenciais"
    headers: dict = field(default_factory=dict)


@dataclass
class ErroAoGerarToken(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Erro ao gerar token."


@dataclass
class CredenciaisIncorretas(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Email ou senha incorretos"
