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
    def __init__(
        self,
        session_factory=DEFAULT_SQL_SESSION_FACTORY,
        session: AsyncSession | None = None,
    ) -> None:
        self.session_factory = session_factory
        self._session_externa = session

    async def __aenter__(self) -> BaseRepoPadrao:
        if self._session_externa:
            self.session = self._session_externa
            self._owns_session = False
        else:
            self.session: AsyncSession = self.session_factory()()
            self._owns_session = True
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        await super().__aexit__(*args)
        if self._owns_session:
            await self.session.close()

    async def _commit(self) -> None:
        if self._owns_session:
            await self.session.commit()
        else:
            await self.session.flush()

    async def rollback(self) -> None:
        if self._owns_session:
            await self.session.rollback()


class RepositorioDominio(BaseRepoPadrao): ...


class RepositorioConsulta(BaseRepoPadrao): ...
