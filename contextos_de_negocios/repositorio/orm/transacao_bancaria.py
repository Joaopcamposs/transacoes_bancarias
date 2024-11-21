from uuid import uuid4

from sqlalchemy import Column, String, Uuid, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from infra.banco_de_dados import Base


class TransacaoBancaria(Base):
    __tablename__ = "transacao_bancaria"

    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    tipo = Column(String, nullable=False)
    valor = Column(Numeric, nullable=False)
    data = Column(DateTime, server_default=func.now())
    numero_da_conta = Column(String, ForeignKey("conta_bancaria.numero_da_conta"))
    numero_da_conta_destino = Column(
        String, ForeignKey("conta_bancaria.numero_da_conta"), nullable=True
    )  # apenas para transferência

    conta = relationship(
        "ContaBancaria", foreign_keys=[numero_da_conta], back_populates="transacoes"
    )
    conta_destino = relationship(
        "ContaBancaria", foreign_keys=[numero_da_conta_destino]
    )
