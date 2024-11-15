from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.repositorio.orm.cliente import Cliente


class RepoClienteLeitura:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[Cliente]:
        clientes = (await session.execute(select(Cliente))).scalars().all()
        return clientes

    @staticmethod
    async def consultar_por_id(session: AsyncSession, id: Uuid) -> Cliente | None:
        cliente = await session.get(Cliente, id)
        return cliente

    @staticmethod
    async def consultar_por_cpf(session: AsyncSession, cpf: str) -> Cliente | None:
        cliente = (
            await session.execute(select(Cliente).filter_by(cpf=cpf))
        ).scalar_one_or_none()
        return cliente
