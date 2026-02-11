from uuid import uuid4

from sqlalchemy import Column, Table, Uuid, String
from sqlalchemy.orm import relationship

from business_contexts.domain.aggregates.client import Client
from infra.database import mapper_registry

client_table: Table = Table(
    "client",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("name", String(255), nullable=False),
    Column("cpf", String(11), nullable=False, index=True, unique=True),
)

client_mapper = mapper_registry.map_imperatively(
    Client,
    client_table,
    properties={
        "accounts": relationship("Account", back_populates="client"),
    },
)
