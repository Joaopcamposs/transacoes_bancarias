from dataclasses import dataclass
from uuid import UUID

from contextos_de_negocios.utils.tipos_basicos import CPF


@dataclass
class Cliente:
    nome: str
    cpf: CPF
    id: UUID | None = None

    @classmethod
    def retornar_agregado_para_cadastro(cls, nome: str, cpf: CPF) -> "Cliente":
        return Cliente(nome=nome, cpf=cpf)

    def cadastrar(self) -> None: ...

    def atualizar(self, nome: str, cpf: CPF) -> None:
        self.nome = nome
        self.cpf = cpf

    def remover(self) -> None: ...
