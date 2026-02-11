from uuid import uuid4

from sqlalchemy import Table, Column, String, ForeignKey, Uuid, Numeric
from sqlalchemy.orm import relationship

from business_contexts.domain.aggregates.bank_account import Account
from infra.database import mapper_registry

bank_account_table: Table = Table(
    "bank_account",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("account_number", String(255), nullable=False, index=True, unique=True),
    Column("balance", Numeric, nullable=False),
    Column("client_cpf", String(11), ForeignKey("client.cpf"), nullable=False),
)

account_mapper = mapper_registry.map_imperatively(
    Account,
    bank_account_table,
    properties={
        "client": relationship("Client", back_populates="accounts"),
        "transactions": relationship(
            "Transaction",
            back_populates="account",
            foreign_keys="[Transaction.account_number]",
        ),
    },
)
