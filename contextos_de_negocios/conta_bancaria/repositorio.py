from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.conta_bancaria.exceptions import ErroAoDeletarContaBancaria
from contextos_de_negocios.conta_bancaria.models import ContaBancaria
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class RepoContaBancariaLeitura:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[ContaBancaria]:
        conta_bancarias = (await session.execute(select(ContaBancaria))).scalars().all()
        return conta_bancarias

    @staticmethod
    async def consultar_por_id(session: AsyncSession, id: Uuid) -> ContaBancaria | None:
        conta_bancaria = await session.get(ContaBancaria, id)
        return conta_bancaria

    @staticmethod
    async def consultar_por_numero_da_conta(
        session: AsyncSession, numero_da_conta: str
    ) -> ContaBancaria | None:
        conta_bancaria = (
            await session.execute(
                select(ContaBancaria).filter_by(numero_da_conta=numero_da_conta)
            )
        ).scalar_one_or_none()
        return conta_bancaria


class RepoContaBancariaEscrita:
    @staticmethod
    async def adicionar(
        session: AsyncSession,
        conta_bancaria: ContaBancaria,
        tipo_operacao: TipoOperacao,
    ) -> ContaBancaria:
        if tipo_operacao == TipoOperacao.INSERCAO:
            try:
                session.add(conta_bancaria)
                await session.commit()
                await session.refresh(conta_bancaria)
            except Exception as erro:
                await session.rollback()
                raise erro
        elif tipo_operacao == TipoOperacao.ATUALIZACAO:
            try:
                await session.merge(conta_bancaria)
                await session.commit()
                await session.refresh(conta_bancaria)
            except Exception as erro:
                await session.rollback()
                raise erro
        return conta_bancaria

    @staticmethod
    async def remover(session: AsyncSession, conta_bancaria: ContaBancaria) -> None:
        try:
            await session.delete(conta_bancaria)
            await session.commit()
        except Exception as erro:
            await session.rollback()
            raise ErroAoDeletarContaBancaria(
                detail=f"Erro ao deletar conta bancaria: {erro}",
            )
