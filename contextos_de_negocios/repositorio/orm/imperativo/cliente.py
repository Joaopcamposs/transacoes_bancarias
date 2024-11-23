from uuid import uuid4

from sqlalchemy import Column, Table, Uuid, String
from sqlalchemy.orm import relationship

from contextos_de_negocios.dominio.agregados.cliente import Cliente
from infra.banco_de_dados import mapper_registry

tabela_cliente = Table(
    "cliente",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("nome", String(255), nullable=False),
    Column("cpf", String(11), nullable=False, index=True, unique=True),
)

cliente_mapper = mapper_registry.map_imperatively(
    Cliente,
    tabela_cliente,
    properties={
        "contas": relationship("Conta", back_populates="cliente"),
    },
)
