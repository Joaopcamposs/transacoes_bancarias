from uuid import uuid4

from sqlalchemy import Table, Column, String, ForeignKey, Uuid, Numeric
from sqlalchemy.orm import relationship

from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from infra.banco_de_dados import mapper_registry

tabela_conta_bancaria = Table(
    "conta_bancaria",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("numero_da_conta", String(255), nullable=False, index=True, unique=True),
    Column("saldo", Numeric, nullable=False),
    Column("cpf_cliente", String(11), ForeignKey("cliente.cpf"), nullable=False),
)

conta_mapper = mapper_registry.map_imperatively(
    Conta,
    tabela_conta_bancaria,
    properties={
        "cliente": relationship("Cliente", back_populates="contas"),
        "transacoes": relationship(
            "Transacao",
            back_populates="conta",
            foreign_keys="[Transacao.numero_da_conta]",
        ),
    },
)
