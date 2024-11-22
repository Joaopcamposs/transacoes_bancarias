from uuid import uuid4

from sqlalchemy import Table, Column, String, ForeignKey, Uuid, Numeric, DateTime, func
from sqlalchemy.orm import relationship

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from infra.banco_de_dados import mapper_registry

tabela_transacao_bancaria = Table(
    "transacao_bancaria",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("tipo", String(255), nullable=False),
    Column("valor", Numeric, nullable=False),
    Column("data", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column(
        "numero_da_conta",
        String(255),
        ForeignKey("conta_bancaria.numero_da_conta"),
        nullable=False,
    ),
    Column(
        "numero_da_conta_destino",
        String(255),
        ForeignKey("conta_bancaria.numero_da_conta"),
        nullable=True,
    ),
)

transacao_bancaria_mapper = mapper_registry.map_imperatively(
    Transacao,
    tabela_transacao_bancaria,
    properties={
        "conta": relationship(
            "Conta",
            foreign_keys=[tabela_transacao_bancaria.c.numero_da_conta],
            back_populates="transacoes",
        ),
        "conta_destino": relationship(
            "Conta",
            foreign_keys=[tabela_transacao_bancaria.c.numero_da_conta_destino],
        ),
    },
)
