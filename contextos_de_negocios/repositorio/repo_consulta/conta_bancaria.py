from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.entidades.conta_bancaria import ContaEntidade
from libs.ddd.adaptadores.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores import Filtros


class ContaBancariaRepoConsulta(RepositorioConsulta):
    async def consultar_por_filtros(self, filtros: Filtros) -> Sequence[ContaEntidade]:
        listar_transacoes = True
        if "listar_transacoes" in filtros:
            listar_transacoes = filtros.get("listar_transacoes")
            filtros.pop("listar_transacoes")

        async with self:
            operacao = select(Conta).filter_by(**filtros)
            if listar_transacoes:
                operacao = operacao.options(joinedload(Conta.transacoes))
            contas = (await self.session.execute(operacao)).unique().scalars().all()

            contas_entidade = []
            for conta in contas:
                transacoes_lista = []
                if listar_transacoes:
                    transacoes_recebidas = (
                        (
                            await self.session.execute(
                                select(Transacao).where(
                                    Transacao.numero_da_conta_destino
                                    == conta.numero_da_conta
                                )
                            )
                        )
                        .scalars()
                        .all()
                    )

                    todas_transacoes = list(conta.transacoes) + list(
                        transacoes_recebidas
                    )
                    todas_transacoes.sort(key=lambda t: t.data, reverse=True)

                    transacoes_lista = [
                        Transacao(
                            id=transacao.id,
                            tipo=transacao.tipo,
                            valor=transacao.valor,
                            data=transacao.data,
                            numero_da_conta=transacao.numero_da_conta,
                            numero_da_conta_destino=transacao.numero_da_conta_destino,
                        )
                        for transacao in todas_transacoes
                    ]

                contas_entidade.append(
                    ContaEntidade(
                        id=conta.id,
                        numero_da_conta=conta.numero_da_conta,
                        saldo=conta.saldo,
                        cpf_cliente=conta.cpf_cliente,
                        transacoes=transacoes_lista,
                    )
                )

        return contas_entidade

    async def consultar_um_por_filtros(self, filtros: Filtros) -> ContaEntidade | None:
        listar_transacoes = True
        if "listar_transacoes" in filtros:
            listar_transacoes = filtros.get("listar_transacoes")
            filtros.pop("listar_transacoes")

        async with self:
            operacao = select(Conta).filter_by(**filtros)
            if listar_transacoes:
                operacao = operacao.options(joinedload(Conta.transacoes))
            conta = (await self.session.execute(operacao)).unique().scalar_one_or_none()
            if not conta:
                return None

            transacoes_lista = []
            if listar_transacoes:
                transacoes_recebidas = (
                    (
                        await self.session.execute(
                            select(Transacao).where(
                                Transacao.numero_da_conta_destino
                                == conta.numero_da_conta
                            )
                        )
                    )
                    .scalars()
                    .all()
                )

                todas_transacoes = list(conta.transacoes) + list(transacoes_recebidas)
                todas_transacoes.sort(key=lambda t: t.data, reverse=True)

                transacoes_lista = [
                    Transacao(
                        id=transacao.id,
                        tipo=transacao.tipo,
                        valor=transacao.valor,
                        data=transacao.data,
                        numero_da_conta=transacao.numero_da_conta,
                        numero_da_conta_destino=transacao.numero_da_conta_destino,
                    )
                    for transacao in todas_transacoes
                ]

            conta_entidade = ContaEntidade(
                id=conta.id,
                numero_da_conta=conta.numero_da_conta,
                saldo=conta.saldo,
                cpf_cliente=conta.cpf_cliente,
                transacoes=transacoes_lista,
            )

        return conta_entidade
