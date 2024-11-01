from typing import Sequence

from sqlalchemy import Uuid, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.conta_bancaria.models import ContaBancaria
from contextos_de_negocios.transacao_bancaria.models import TransacaoBancaria
from contextos_de_negocios.transacao_bancaria.objetos_de_valor import TipoTransacao


class RepoTransacaoBancariaLeitura:
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


class RepoTransacaoBancariaEscrita:
    @staticmethod
    async def adicionar(
        session: AsyncSession,
        transacao_bancaria: TransacaoBancaria,
    ) -> TransacaoBancaria:
        try:
            session.add(transacao_bancaria)

            valor_movimentado = transacao_bancaria.valor
            if transacao_bancaria.tipo in [
                TipoTransacao.SAQUE.value,
                TipoTransacao.TRANSFERENCIA.value,
            ]:
                valor_movimentado *= -1

            atualizar_saldo_conta_origem = (
                update(ContaBancaria)
                .where(
                    ContaBancaria.numero_da_conta == transacao_bancaria.numero_da_conta
                )
                .values(saldo=ContaBancaria.saldo + valor_movimentado)
            )
            await session.execute(atualizar_saldo_conta_origem)

            if transacao_bancaria.numero_da_conta_destino:
                atualizar_saldo_conta_destino = (
                    update(ContaBancaria)
                    .where(
                        ContaBancaria.numero_da_conta
                        == transacao_bancaria.numero_da_conta_destino
                    )
                    .values(saldo=ContaBancaria.saldo + transacao_bancaria.valor)
                )
                await session.execute(atualizar_saldo_conta_destino)

            await session.commit()
            await session.refresh(transacao_bancaria)
        except Exception as erro:
            await session.rollback()
            raise erro
        return transacao_bancaria
