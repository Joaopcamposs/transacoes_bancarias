from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from contextos_de_negocios.dominio.entidades.conta_bancaria import ContaEntidade
from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from libs.ddd.adaptadores.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores import Filtros


class ContaBancariaRepoConsulta(RepositorioConsulta):
    async def consultar_por_filtros(self, filtros: Filtros) -> Sequence[ContaEntidade]:
        async with self:
            contas = (
                (
                    await self.session.execute(
                        select(ContaBancaria)
                        .options(joinedload(ContaBancaria.transacoes))
                        .filter_by(**filtros)
                    )
                )
                .unique()
                .scalars()
                .all()
            )

            contas_entidade = [
                ContaEntidade(
                    id=conta.id,
                    numero_da_conta=conta.numero_da_conta,
                    saldo=conta.saldo,
                    cpf_cliente=conta.cpf_cliente,
                    transacoes=conta.transacoes,
                )
                for conta in contas
            ]

        return contas_entidade

    async def consultar_um_por_filtros(self, filtros: Filtros) -> ContaEntidade | None:
        async with self:
            conta = (
                (
                    await self.session.execute(
                        select(ContaBancaria)
                        .options(joinedload(ContaBancaria.transacoes))
                        .filter_by(**filtros)
                    )
                )
                .unique()
                .scalar_one_or_none()
            )
            if not conta:
                return None

            conta_entidade = ContaEntidade(
                id=conta.id,
                numero_da_conta=conta.numero_da_conta,
                saldo=conta.saldo,
                cpf_cliente=conta.cpf_cliente,
                transacoes=conta.transacoes,
            )

        return conta_entidade
