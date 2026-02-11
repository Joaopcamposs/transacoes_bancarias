from uuid import uuid4

from sqlalchemy import Column, Table, Uuid, String, Boolean

from business_contexts.domain.aggregates.user import User
from infra.database import mapper_registry

user_table: Table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True, index=True, default=uuid4),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, index=True, unique=True),
    Column("password", String(255), nullable=False),
    Column("is_admin", Boolean, nullable=False, default=False),
    Column("is_active", Boolean, nullable=False, default=True),
)

user_mapper = mapper_registry.map_imperatively(
    User,
    user_table,
)
