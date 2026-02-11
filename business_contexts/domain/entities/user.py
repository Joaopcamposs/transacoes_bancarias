from dataclasses import dataclass

from pydantic import BaseModel, UUID4


class CreateUser(BaseModel):
    """Modelo de entrada para cadastro de usuário."""

    name: str
    email: str
    password: str
    is_admin: bool
    is_active: bool


class UpdateUser(BaseModel):
    """Modelo de entrada para atualização de usuário."""

    name: str
    email: str
    password: str
    is_admin: bool
    is_active: bool
    _id: UUID4 | None = None


class ReadUser(BaseModel):
    """Modelo de saída para leitura de usuário."""

    id: UUID4
    name: str
    email: str
    is_admin: bool
    is_active: bool


@dataclass
class UserEntity:
    """Entidade que representa um usuário consultado do banco de dados."""

    id: UUID4
    name: str
    email: str
    is_admin: bool
    is_active: bool
    _password: str
