from decimal import Decimal
from uuid import UUID

from sqlalchemy import update, insert, select

from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.exceptions import (
    SaldoInsuficienteParaRealizarTransacao,
)
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from infra.concorrencia import gerenciador_locks
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class TransacaoBancariaRepoDominio(RepositorioDominio):
    async def adicionar(
        self,
        transacao: Transacao,
    ) -> UUID:
        # Lock em memória para SQLite (em produção com PostgreSQL, FOR UPDATE cuida disso)
        async with gerenciador_locks.bloquear_contas(
            transacao.numero_da_conta, transacao.numero_da_conta_destino or ""
        ):
            async with self:
                try:
                    # Bloqueio explícito das contas para evitar problemas de concorrência
                    # IMPORTANTE: Bloqueio DEVE ocorrer ANTES de qualquer validação de saldo
                    saldo_origem = await self.__bloquear_e_obter_saldo(
                        transacao.numero_da_conta, transacao.numero_da_conta_destino
                    )

                    # Validar saldo DENTRO da transação, após o bloqueio
                    if transacao.tipo in [
                        TipoTransacao.SAQUE,
                        TipoTransacao.TRANSFERENCIA,
                    ]:
                        if saldo_origem < transacao.valor:
                            raise SaldoInsuficienteParaRealizarTransacao

                    dados = {
                        "tipo": transacao.tipo.value,
                        "valor": transacao.valor,
                        "data": transacao.data,
                        "numero_da_conta": transacao.numero_da_conta,
                        "numero_da_conta_destino": transacao.numero_da_conta_destino,
                    }
                    operacao = insert(Transacao).values(dados).returning(Transacao.id)
                    resultado = await self.session.execute(operacao)

                    # tratar valor movimentado de acordo com o tipo de transacao
                    valor_movimentado = transacao.valor
                    if transacao.tipo in [
                        TipoTransacao.SAQUE,
                        TipoTransacao.TRANSFERENCIA,
                    ]:
                        valor_movimentado *= -1

                    atualizar_saldo_conta_origem = (
                        update(Conta)
                        .where(Conta.numero_da_conta == transacao.numero_da_conta)
                        .values(saldo=Conta.saldo + valor_movimentado)
                    )
                    await self.session.execute(atualizar_saldo_conta_origem)

                    if transacao.numero_da_conta_destino:
                        atualizar_saldo_conta_destino = (
                            update(Conta)
                            .where(
                                Conta.numero_da_conta
                                == transacao.numero_da_conta_destino
                            )
                            .values(saldo=Conta.saldo + transacao.valor)
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

    async def __bloquear_e_obter_saldo(
        self, numero_da_conta_origem: str, numero_da_conta_destino: str | None = None
    ) -> Decimal:
        """Bloqueia as contas envolvidas e retorna o saldo atual da conta origem.

        IMPORTANTE: Ordena os locks por numero_da_conta para evitar deadlocks
        em transferências bidirecionais (A→B e B→A simultâneas).
        """
        contas_para_bloquear = [numero_da_conta_origem]
        if numero_da_conta_destino:
            contas_para_bloquear.append(numero_da_conta_destino)

        # Ordenar para evitar deadlock
        contas_para_bloquear.sort()

        saldo_origem = Decimal("0.00")

        for numero_conta in contas_para_bloquear:
            query = (
                select(Conta)
                .where(Conta.numero_da_conta == numero_conta)
                .with_for_update()
            )
            resultado = await self.session.execute(query)
            conta = resultado.scalar_one_or_none()

            if conta and numero_conta == numero_da_conta_origem:
                saldo_origem = conta.saldo

        return saldo_origem
