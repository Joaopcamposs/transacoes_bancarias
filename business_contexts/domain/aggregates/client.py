from dataclasses import dataclass
from uuid import UUID

from business_contexts.utils.base_types import CPF
from libs.ddd.domain.aggregate import Aggregate


@dataclass
class Client(Aggregate):
    """Agregado raiz que representa um cliente no sistema bancário."""

    name: str
    cpf: CPF
    id: UUID | None = None

    @classmethod
    def return_aggregate_for_creation(cls, name: str, cpf: CPF) -> "Client":
        """Retorna uma instância do agregado Client preparada para cadastro."""
        return Client(name=name, cpf=cpf)

    def create(self) -> None:
        """Executa a lógica de criação do cliente."""
        ...

    def update(self, name: str, cpf: CPF) -> None:
        """Atualiza os dados do cliente."""
        self.name = name
        self.cpf = cpf

    def remove(self) -> None:
        """Executa a lógica de remoção do cliente."""
        ...
