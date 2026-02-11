from typing import Sequence

from sqlalchemy import select

from business_contexts.domain.aggregates.client import Client
from business_contexts.domain.entities.client import ClientEntity
from libs.ddd.adapters.repository import QueryRepository
from libs.ddd.adapters.viewers import Filters


class ClientQueryRepo(QueryRepository):
    """Repositório de consulta para clientes."""

    async def query_by_filters(self, filters: Filters) -> Sequence[ClientEntity]:
        """Consulta clientes aplicando os filtros fornecidos."""
        async with self:
            clients = (
                (await self.session.execute(select(Client).filter_by(**filters)))
                .scalars()
                .all()
            )

            client_entities: list[ClientEntity] = [
                ClientEntity(
                    id=client.id,
                    name=client.name,
                    cpf=client.cpf,
                )
                for client in clients
            ]

        return client_entities

    async def query_one_by_filters(self, filters: Filters) -> ClientEntity | None:
        """Consulta um único cliente aplicando os filtros fornecidos."""
        async with self:
            client = (
                await self.session.execute(select(Client).filter_by(**filters))
            ).scalar_one_or_none()
            if not client:
                return None

            client_entity = ClientEntity(
                id=client.id,
                name=client.name,
                cpf=client.cpf,
            )

        return client_entity
