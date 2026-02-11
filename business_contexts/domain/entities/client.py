from dataclasses import dataclass

from pydantic import BaseModel, UUID4


class CreateClient(BaseModel):
    """Modelo de entrada para cadastro de cliente."""

    name: str
    cpf: str


class UpdateClient(BaseModel):
    """Modelo de entrada para atualização de cliente."""

    name: str
    cpf: str
    _id: UUID4 | None = None


class ReadClient(BaseModel):
    """Modelo de saída para leitura de cliente."""

    id: UUID4
    name: str
    cpf: str


@dataclass(frozen=True)
class ClientEntity:
    """Entidade imutável que representa um cliente consultado do banco de dados."""

    id: UUID4
    name: str
    cpf: str
