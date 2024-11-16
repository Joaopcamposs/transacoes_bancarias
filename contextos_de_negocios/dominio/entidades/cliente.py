from dataclasses import dataclass

from pydantic import BaseModel, UUID4


class CadastrarCliente(BaseModel):
    nome: str
    cpf: str


class AtualizarCliente(BaseModel):
    nome: str
    cpf: str
    _id: UUID4 | None = None

    class Config:
        underscore_attrs_are_private = True  # Torna os atributos com "_" privados


class LerCliente(BaseModel):
    id: UUID4
    nome: str
    cpf: str


@dataclass(frozen=True)
class ClienteEntidade:
    id: UUID4
    nome: str
    cpf: str
