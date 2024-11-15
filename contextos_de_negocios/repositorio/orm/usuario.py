from uuid import uuid4

from sqlalchemy import Column, Uuid, String, Boolean

from infra.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Uuid, primary_key=True, unique=True, default=uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    senha = Column(String, nullable=False)
    adm = Column(Boolean, nullable=False, default=False)
    ativo = Column(Boolean, nullable=False, default=True)
