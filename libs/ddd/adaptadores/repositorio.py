from __future__ import annotations

from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY


class AbstractRepo(ABC):
    async def __aenter__(self) -> AbstractRepo:
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()

    async def commit(self) -> None:
        await self._commit()

    @abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class BaseRepoPadrao(AbstractRepo):
    def __init__(self, session_factory=DEFAULT_SQL_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> BaseRepoPadrao:
        self.session: AsyncSession = self.session_factory()()
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class RepositorioDominio(BaseRepoPadrao): ...


class RepositorioConsulta(BaseRepoPadrao): ...
