from uuid import uuid4

from sqlalchemy import Column, Uuid, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from contextos_de_negocios.transacao_bancaria.models import TransacaoBancaria
from infra.database import Base


class ContaBancaria(Base):
    __tablename__ = "conta_bancaria"

    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    numero_da_conta = Column(String, index=True, unique=True)
    saldo = Column(Numeric)

    # Chave estrangeira para o Cliente
    cpf_cliente = Column(String, ForeignKey("cliente.cpf"))

    # Relacionamento com Cliente
    cliente = relationship("Cliente", back_populates="contas")
    # Relacionamento com TransacaoBancaria
    transacoes = relationship(
        TransacaoBancaria,
        back_populates="conta",
        foreign_keys="[TransacaoBancaria.numero_da_conta]",
    )
