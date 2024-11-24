from uuid import UUID

from sqlalchemy import update, insert, select

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from contextos_de_negocios.repositorio.orm.declarativo.conta_bancaria import (
    ContaBancariaDB,
)
from contextos_de_negocios.repositorio.orm.declarativo.transacao_bancaria import (
    TransacaoBancariaDB,
)
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class TransacaoBancariaRepoDominio(RepositorioDominio):
    async def adicionar(
        self,
        transacao: Transacao,
    ) -> UUID:
        async with self:
            try:
                # Bloqueio explícito das contas para evitar problemas de concorrência
                await self.__bloquear_contas_para_concorrencia(
                    transacao.numero_da_conta, transacao.numero_da_conta_destino
                )

                dados = {
                    "tipo": transacao.tipo.value,
                    "valor": transacao.valor,
                    "data": transacao.data,
                    "numero_da_conta": transacao.numero_da_conta,
                    "numero_da_conta_destino": transacao.numero_da_conta_destino,
                }
                operacao = (
                    insert(TransacaoBancariaDB)
                    .values(dados)
                    .returning(TransacaoBancariaDB.id)
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
                    update(ContaBancariaDB)
                    .where(ContaBancariaDB.numero_da_conta == transacao.numero_da_conta)
                    .values(saldo=ContaBancariaDB.saldo + valor_movimentado)
                )
                await self.session.execute(atualizar_saldo_conta_origem)

                if transacao.numero_da_conta_destino:
                    atualizar_saldo_conta_destino = (
                        update(ContaBancariaDB)
                        .where(
                            ContaBancariaDB.numero_da_conta
                            == transacao.numero_da_conta_destino
                        )
                        .values(saldo=ContaBancariaDB.saldo + transacao.valor)
                    )
                    await self.session.execute(atualizar_saldo_conta_destino)

                await self.commit()
            except Exception as erro:
                await self.rollback()
                raise erro

            id_resultado: UUID | None = transacao.id
            if not id_resultado:
                id_resultado = resultado.scalar_one_or_none()

        return id_resultado

    async def __bloquear_contas_para_concorrencia(
        self, numero_da_conta_origem: str, numero_da_conta_destino: str | None = None
    ) -> None:
        bloquear_conta_origem = (
            select(ContaBancariaDB)
            .where(ContaBancariaDB.numero_da_conta == numero_da_conta_origem)
            .with_for_update()
        )
        await self.session.execute(bloquear_conta_origem)

        if numero_da_conta_destino:
            bloquear_conta_destino = (
                select(ContaBancariaDB)
                .where(ContaBancariaDB.numero_da_conta == numero_da_conta_destino)
                .with_for_update()
            )
            await self.session.execute(bloquear_conta_destino)
