from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY


class Repositorio(ABC):
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session or DEFAULT_SQL_SESSION_FACTORY

    async def __aenter__(self) -> "Repositorio":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.session.close()


class RepositorioDominio(Repositorio):
    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class RepositorioConsulta(Repositorio): ...
