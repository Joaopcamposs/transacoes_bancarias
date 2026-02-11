from uuid import uuid4

from sqlalchemy import Table, Column, String, ForeignKey, Uuid, Numeric, DateTime, func
from sqlalchemy.orm import relationship

from business_contexts.domain.aggregates.bank_transaction import Transaction
from infra.database import mapper_registry

bank_transaction_table: Table = Table(
    "bank_transaction",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("type", String(255), nullable=False),
    Column("amount", Numeric, nullable=False),
    Column("date", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column(
        "account_number",
        String(255),
        ForeignKey("bank_account.account_number"),
        nullable=False,
    ),
    Column(
        "destination_account_number",
        String(255),
        ForeignKey("bank_account.account_number"),
        nullable=True,
    ),
)

bank_transaction_mapper = mapper_registry.map_imperatively(
    Transaction,
    bank_transaction_table,
    properties={
        "account": relationship(
            "Account",
            foreign_keys=[bank_transaction_table.c.account_number],
            back_populates="transactions",
        ),
        "destination_account": relationship(
            "Account",
            foreign_keys=[bank_transaction_table.c.destination_account_number],
        ),
    },
)
