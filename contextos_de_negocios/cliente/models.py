from uuid import uuid4

from sqlalchemy import Column, Uuid, String
from sqlalchemy.orm import relationship

from contextos_de_negocios.conta_bancaria.models import ContaBancaria
from infra.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    nome = Column(String)
    cpf = Column(String, index=True, unique=True)

    # Relacionamento com ContaBancaria
    contas = relationship(ContaBancaria, back_populates="cliente")
