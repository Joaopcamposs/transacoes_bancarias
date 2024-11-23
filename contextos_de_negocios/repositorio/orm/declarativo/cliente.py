from uuid import uuid4

from sqlalchemy import Column, Uuid, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from contextos_de_negocios.repositorio.orm.declarativo.conta_bancaria import (
    ContaBancariaDB,
)
from infra.banco_de_dados import Base


class ClienteDB(Base):
    __tablename__ = "cliente"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, index=True, default=uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = Column(String(255), nullable=False, index=True, unique=True)

    # Relacionamento com ContaBancaria
    contas: Mapped["ContaBancariaDB"] = relationship(
        ContaBancariaDB, back_populates="cliente"
    )
