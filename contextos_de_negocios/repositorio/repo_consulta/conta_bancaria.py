from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria


class ContaBancariaRepoConsulta:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[ContaBancaria]:
        conta_bancarias = (
            (
                await session.execute(
                    select(ContaBancaria).options(joinedload(ContaBancaria.transacoes))
                )
            )
            .scalars()
            .unique()
            .all()
        )
        return conta_bancarias

    @staticmethod
    async def consultar_por_id(session: AsyncSession, id: Uuid) -> ContaBancaria | None:
        conta_bancaria = (
            (
                await session.execute(
                    select(ContaBancaria)
                    .options(joinedload(ContaBancaria.transacoes))
                    .filter_by(id=id)
                )
            )
            .unique()
            .scalar_one_or_none()
        )
        return conta_bancaria

    @staticmethod
    async def consultar_por_numero_da_conta(
        session: AsyncSession, numero_da_conta: str
    ) -> ContaBancaria | None:
        conta_bancaria = (
            (
                await session.execute(
                    select(ContaBancaria)
                    .options(joinedload(ContaBancaria.transacoes))
                    .filter_by(numero_da_conta=numero_da_conta)
                )
            )
            .unique()
            .scalar_one_or_none()
        )
        return conta_bancaria
