from typing import Sequence

from sqlalchemy import select

from contextos_de_negocios.dominio.agregados.cliente import Cliente
from contextos_de_negocios.dominio.entidades.cliente import ClienteEntidade
from libs.ddd.adaptadores.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores import Filtros


class ClienteRepoConsulta(RepositorioConsulta):
    async def consultar_por_filtros(
        self, filtros: Filtros
    ) -> Sequence[ClienteEntidade]:
        async with self:
            clientes = (
                (await self.session.execute(select(Cliente).filter_by(**filtros)))
                .scalars()
                .all()
            )

            clientes_entidade = [
                ClienteEntidade(
                    id=cliente.id,
                    nome=cliente.nome,
                    cpf=cliente.cpf,
                )
                for cliente in clientes
            ]

        return clientes_entidade

    async def consultar_um_por_filtros(
        self, filtros: Filtros
    ) -> ClienteEntidade | None:
        async with self:
            cliente = (
                await self.session.execute(select(Cliente).filter_by(**filtros))
            ).scalar_one_or_none()
            if not cliente:
                return None

            cliente_entidade = ClienteEntidade(
                id=cliente.id,
                nome=cliente.nome,
                cpf=cliente.cpf,
            )

        return cliente_entidade
