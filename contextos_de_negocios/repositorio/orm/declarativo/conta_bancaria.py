from decimal import Decimal
from uuid import uuid4

from sqlalchemy import Uuid, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from contextos_de_negocios.repositorio.orm.declarativo.cliente import ClienteDB
from contextos_de_negocios.repositorio.orm.declarativo.transacao_bancaria import (
    TransacaoBancariaDB,
)
from infra.banco_de_dados import Base


class ContaBancariaDB(Base):
    __tablename__ = "conta_bancaria"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, index=True, default=uuid4)
    numero_da_conta: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    saldo: Mapped[Decimal] = mapped_column(Numeric)

    # Chave estrangeira para o Cliente
    cpf_cliente: Mapped[str] = mapped_column(String(11), ForeignKey("cliente.cpf"))

    # Relacionamento com Cliente
    cliente: Mapped["ClienteDB"] = relationship("ClienteDB", back_populates="contas")
    # Relacionamento com TransacaoBancaria
    transacoes: Mapped[list["TransacaoBancariaDB"]] = relationship(
        TransacaoBancariaDB,
        back_populates="conta",
        foreign_keys="[TransacaoBancariaDB.numero_da_conta]",
    )
