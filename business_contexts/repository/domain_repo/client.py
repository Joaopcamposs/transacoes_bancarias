from uuid import UUID

from sqlalchemy import insert, update, delete, Uuid, select

from business_contexts.domain.aggregates.client import Client
from business_contexts.utils.base_types import OperationType
from libs.ddd.adapters.repository import DomainRepository


class ClientDomainRepo(DomainRepository):
    """Repositório de domínio para operações de escrita de clientes."""

    async def query_by_id(self, id: Uuid) -> Client | None:
        """Consulta um cliente pelo ID."""
        async with self:
            client = (
                await self.session.execute(select(Client).where(Client.id == id))
            ).scalar_one_or_none()

            if not client:
                return None

            aggregate = Client(
                id=client.id,
                name=client.name,
                cpf=client.cpf,
            )
        return aggregate

    async def add(
        self,
        client: Client,
        operation_type: OperationType,
    ) -> UUID:
        """Adiciona ou atualiza um cliente no banco de dados."""
        async with self:
            try:
                data: dict = {
                    "name": client.name,
                    "cpf": client.cpf,
                }

                match operation_type:
                    case OperationType.INSERT:
                        operation = insert(Client).values(data).returning(Client.id)
                        result = await self.session.execute(operation)

                    case OperationType.UPDATE:
                        operation = (
                            update(Client).where(Client.id == client.id).values(data)
                        )
                        await self.session.execute(operation)

                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error

            result_id: UUID | None = client.id
            if not result_id:
                result_id = result.scalar_one_or_none()

        return result_id

    async def remove(self, client: Client) -> None:
        """Remove um cliente do banco de dados."""
        async with self:
            try:
                operation = delete(Client).where(Client.id == client.id)

                await self.session.execute(operation)
                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error
