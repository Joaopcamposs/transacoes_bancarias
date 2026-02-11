from uuid import UUID

from sqlalchemy import Uuid, select, insert, update, delete

from business_contexts.domain.aggregates.user import User
from business_contexts.utils.base_types import OperationType
from libs.ddd.adapters.repository import DomainRepository


class UserDomainRepo(DomainRepository):
    """Repositório de domínio para operações de escrita de usuários."""

    async def query_by_id(self, id: Uuid) -> User | None:
        """Consulta um usuário pelo ID."""
        async with self:
            user = (
                await self.session.execute(select(User).where(User.id == id))
            ).scalar_one_or_none()

            if not user:
                return None

            aggregate = User(
                id=user.id,
                name=user.name,
                email=user.email,
                is_admin=user.is_admin,
                is_active=user.is_active,
                password=user.password,
            )
        return aggregate

    async def query_by_email(self, email: str) -> User | None:
        """Consulta um usuário pelo email."""
        async with self:
            user = (
                await self.session.execute(select(User).where(User.email == email))
            ).scalar_one_or_none()

            if not user:
                return None

            aggregate = User(
                id=user.id,
                name=user.name,
                email=user.email,
                is_admin=user.is_admin,
                is_active=user.is_active,
                password=user.password,
            )
        return aggregate

    async def add(
        self,
        user: User,
        operation_type: OperationType,
    ) -> UUID:
        """Adiciona ou atualiza um usuário no banco de dados."""
        async with self:
            try:
                data: dict = {
                    "name": user.name,
                    "email": user.email,
                    "password": user.password,
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                }

                match operation_type:
                    case OperationType.INSERT:
                        operation = insert(User).values(data).returning(User.id)
                        result = await self.session.execute(operation)

                    case OperationType.UPDATE:
                        operation = update(User).where(User.id == user.id).values(data)
                        await self.session.execute(operation)

                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error

            result_id: UUID | None = user.id
            if not result_id:
                result_id = result.scalar_one_or_none()

        return result_id

    async def remove(self, user: User) -> None:
        """Remove um usuário do banco de dados."""
        async with self:
            try:
                operation = delete(User).where(User.id == user.id)

                await self.session.execute(operation)
                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error
