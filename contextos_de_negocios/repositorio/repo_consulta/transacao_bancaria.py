from typing import Sequence

from sqlalchemy import select

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.entidades.transacao_bancaria import TransacaoEntidade
from libs.ddd.adaptadores.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores import Filtros


class TransacaoBancariaRepoConsulta(RepositorioConsulta):
    async def consultar_por_filtros(
        self, filtros: Filtros
    ) -> Sequence[TransacaoEntidade]:
        async with self:
            transacaos = (
                (await self.session.execute(select(Transacao).filter_by(**filtros)))
                .scalars()
                .all()
            )

            transacaos_entidade = [
                TransacaoEntidade(
                    id=transacao.id,
                    tipo=transacao.tipo,
                    valor=transacao.valor,
                    data=transacao.data,
                    numero_da_conta=transacao.numero_da_conta,
                    numero_da_conta_destino=transacao.numero_da_conta_destino,
                )
                for transacao in transacaos
            ]

        return transacaos_entidade

    async def consultar_um_por_filtros(
        self, filtros: Filtros
    ) -> TransacaoEntidade | None:
        transacao = (
            await self.session.execute(select(Transacao).filter_by(**filtros))
        ).scalar_one_or_none()
        if not transacao:
            return None

        transacao_entidade = TransacaoEntidade(
            id=transacao.id,
            tipo=transacao.tipo,
            valor=transacao.valor,
            data=transacao.data,
            numero_da_conta=transacao.numero_da_conta,
            numero_da_conta_destino=transacao.numero_da_conta_destino,
        )

        return transacao_entidade
