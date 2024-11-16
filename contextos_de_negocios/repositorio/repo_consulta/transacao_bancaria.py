from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.repositorio.orm.transacao_bancaria import TransacaoBancaria


class TransacaoBancariaRepoConsulta:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[TransacaoBancaria]:
        transacao_bancarias = (
            (await session.execute(select(TransacaoBancaria))).scalars().all()
        )
        return transacao_bancarias

    @staticmethod
    async def consultar_por_id(
        session: AsyncSession, id: Uuid
    ) -> TransacaoBancaria | None:
        transacao_bancaria = await session.get(TransacaoBancaria, id)
        return transacao_bancaria
