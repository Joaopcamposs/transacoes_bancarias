from uuid import UUID

from sqlalchemy import update, insert

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from contextos_de_negocios.repositorio.orm.transacao_bancaria import TransacaoBancaria
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class TransacaoBancariaRepoDominio(RepositorioDominio):
    async def adicionar(
        self,
        transacao: Transacao,
    ) -> UUID:
        try:
            dados = {
                "tipo": transacao.tipo.value,
                "valor": transacao.valor,
                "data": transacao.data,
                "numero_da_conta": transacao.numero_da_conta,
                "numero_da_conta_destino": transacao.numero_da_conta_destino,
            }
            operacao = (
                insert(TransacaoBancaria).values(dados).returning(TransacaoBancaria.id)
            )
            resultado = await self.session.execute(operacao)

            # tratar valor movimentado de acordo com o tipo de transacao
            valor_movimentado = transacao.valor
            if transacao.tipo in [
                TipoTransacao.SAQUE,
                TipoTransacao.TRANSFERENCIA,
            ]:
                valor_movimentado *= -1

            atualizar_saldo_conta_origem = (
                update(ContaBancaria)
                .where(ContaBancaria.numero_da_conta == transacao.numero_da_conta)
                .values(saldo=ContaBancaria.saldo + valor_movimentado)
            )
            await self.session.execute(atualizar_saldo_conta_origem)

            if transacao.numero_da_conta_destino:
                atualizar_saldo_conta_destino = (
                    update(ContaBancaria)
                    .where(
                        ContaBancaria.numero_da_conta
                        == transacao.numero_da_conta_destino
                    )
                    .values(saldo=ContaBancaria.saldo + transacao.valor)
                )
                await self.session.execute(atualizar_saldo_conta_destino)

            await self.session.commit()
        except Exception as erro:
            await self.session.rollback()
            raise erro

        id_resultado: UUID | None = transacao.id
        if not id_resultado:
            id_resultado = resultado.scalar_one_or_none()

        return id_resultado
