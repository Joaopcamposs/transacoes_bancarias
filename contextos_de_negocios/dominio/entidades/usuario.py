from dataclasses import dataclass

from pydantic import BaseModel, UUID4


class CadastrarUsuario(BaseModel):
    nome: str
    email: str
    senha: str
    adm: bool
    ativo: bool


class AtualizarUsuario(BaseModel):
    nome: str
    email: str
    senha: str
    adm: bool
    ativo: bool
    _senha: str | None = None


class LerUsuario(BaseModel):
    id: UUID4
    nome: str
    email: str
    adm: bool
    ativo: bool


@dataclass
class UsuarioEntidade:
    id: UUID4
    nome: str
    email: str
    adm: bool
    ativo: bool
    _senha: str
