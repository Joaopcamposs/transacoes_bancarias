from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.entidades.cliente import ClienteEntidade
from contextos_de_negocios.repositorio.orm.cliente import Cliente
from libs.ddd.adaptadores.visualizadores import Filtros


class ClienteRepoConsulta:
    @staticmethod
    async def consultar_por_cpf(
        session: AsyncSession, cpf: str
    ) -> ClienteEntidade | None:
        cliente = (
            await session.execute(select(Cliente).filter_by(cpf=cpf))
        ).scalar_one_or_none()
        if not cliente:
            return None

        cliente_entidade = ClienteEntidade(
            id=cliente.id,
            nome=cliente.nome,
            cpf=cliente.cpf,
        )

        return cliente_entidade

    @staticmethod
    async def consultar_por_filtros(
        session: AsyncSession, filtros: Filtros
    ) -> Sequence[Cliente]:
        cliente = (
            (await session.execute(select(Cliente).filter_by(**filtros)))
            .scalars()
            .all()
        )
        return cliente

    @staticmethod
    async def consultar_um_por_filtros(
        session: AsyncSession, filtros: Filtros
    ) -> Cliente | None:
        cliente = (
            await session.execute(select(Cliente).filter_by(**filtros))
        ).scalar_one_or_none()
        return cliente
