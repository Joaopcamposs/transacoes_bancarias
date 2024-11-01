from pydantic import BaseModel, UUID4


class CadastrarEAtualizarUsuario(BaseModel):
    nome: str
    email: str
    senha: str
    adm: bool
    ativo: bool


class LerUsuario(BaseModel):
    id: UUID4
    nome: str
    email: str
    adm: bool
    ativo: bool
