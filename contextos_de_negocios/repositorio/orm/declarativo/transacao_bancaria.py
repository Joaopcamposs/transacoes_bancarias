from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import String, Uuid, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from contextos_de_negocios.repositorio.orm.declarativo.conta_bancaria import (
    ContaBancariaDB,
)
from infra.banco_de_dados import Base


class TransacaoBancariaDB(Base):
    __tablename__ = "transacao_bancaria"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, index=True, default=uuid4)
    tipo: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    numero_da_conta: Mapped[str] = mapped_column(
        String(255), ForeignKey("conta_bancaria.numero_da_conta")
    )
    numero_da_conta_destino: Mapped[str] = mapped_column(
        String(255), ForeignKey("conta_bancaria.numero_da_conta"), nullable=True
    )  # apenas para transferência

    conta: Mapped["ContaBancariaDB"] = relationship(
        "ContaBancariaDB", foreign_keys=[numero_da_conta], back_populates="transacoes"
    )
    conta_destino: Mapped["ContaBancariaDB"] = relationship(
        "ContaBancariaDB", foreign_keys=[numero_da_conta_destino]
    )
