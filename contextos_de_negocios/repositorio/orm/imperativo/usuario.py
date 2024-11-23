from uuid import uuid4

from sqlalchemy import Column, Table, Uuid, String, Boolean

from contextos_de_negocios.dominio.agregados.usuario import Usuario
from infra.banco_de_dados import mapper_registry

tabela_usuario = Table(
    "usuario",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("nome", String(255), nullable=False),
    Column("email", String(255), nullable=False, index=True, unique=True),
    Column("senha", String(255), nullable=False),
    Column("adm", Boolean, nullable=False, default=False),
    Column("ativo", Boolean, nullable=False, default=True),
)

usuario_mapper = mapper_registry.map_imperatively(
    Usuario,
    tabela_usuario,
)
