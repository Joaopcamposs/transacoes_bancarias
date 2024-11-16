from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.repositorio.orm.usuario import Usuario


class UsuarioRepoConsulta:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[Usuario]:
        usuarios = (await session.execute(select(Usuario))).scalars().all()
        return usuarios

    @staticmethod
    async def consultar_por_id(session: AsyncSession, id: Uuid) -> Usuario | None:
        usuario = await session.get(Usuario, id)
        return usuario

    @staticmethod
    async def consultar_por_email(session: AsyncSession, email: str) -> Usuario | None:
        usuario = (
            await session.execute(select(Usuario).filter_by(email=email.lower()))
        ).scalar_one_or_none()
        return usuario
