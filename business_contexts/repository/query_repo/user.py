from typing import Sequence

from sqlalchemy import select

from business_contexts.domain.aggregates.user import User
from business_contexts.domain.entities.user import UserEntity
from libs.ddd.adapters.repository import QueryRepository
from libs.ddd.adapters.viewers import Filters


class UserQueryRepo(QueryRepository):
    """Repositório de consulta para usuários."""

    async def query_by_filters(self, filters: Filters) -> Sequence[UserEntity]:
        """Consulta usuários aplicando os filtros fornecidos."""
        async with self:
            users = (
                (await self.session.execute(select(User).filter_by(**filters)))
                .scalars()
                .all()
            )

            user_entities: list[UserEntity] = [
                UserEntity(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    is_admin=user.is_admin,
                    is_active=user.is_active,
                    _password=user.password,
                )
                for user in users
            ]

        return user_entities

    async def query_one_by_filters(self, filters: Filters) -> UserEntity | None:
        """Consulta um único usuário aplicando os filtros fornecidos."""
        async with self:
            user = (
                await self.session.execute(select(User).filter_by(**filters))
            ).scalar_one_or_none()
            if not user:
                return None

            user_entity = UserEntity(
                id=user.id,
                name=user.name,
                email=user.email,
                is_admin=user.is_admin,
                is_active=user.is_active,
                _password=user.password,
            )

        return user_entity
