from pydantic import BaseModel, UUID4


class CadastrarEAtualizarCliente(BaseModel):
    nome: str
    cpf: str


class LerCliente(BaseModel):
    id: UUID4
    nome: str
    cpf: str
