from uuid import uuid4

from sqlalchemy import Uuid, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from infra.banco_de_dados import Base


class UsuarioDB(Base):
    __tablename__ = "usuario"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, unique=True, default=uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    adm: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
