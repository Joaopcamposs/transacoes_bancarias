from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from contextos_de_negocios.repositorio.orm.transacao_bancaria import TransacaoBancaria
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)


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
