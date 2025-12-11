from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from contextos_de_negocios.repositorio.repo_dominio.conta_bancaria import (
        ContaBancariaRepoDominio,
    )
    from contextos_de_negocios.repositorio.repo_dominio.transacao_bancaria import (
        TransacaoBancariaRepoDominio,
    )


class AbstractUnitOfWork(ABC):
    contas: ContaBancariaRepoDominio
    transacoes: TransacaoBancariaRepoDominio

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SQL_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()()

        # Import here to avoid circular dependencies if any,
        # but ideally should be at top if clean.
        # Doing lazy import for repositories to ensure they get the session.
        from contextos_de_negocios.repositorio.repo_dominio.conta_bancaria import (
            ContaBancariaRepoDominio,
        )
        from contextos_de_negocios.repositorio.repo_dominio.transacao_bancaria import (
            TransacaoBancariaRepoDominio,
        )

        self.contas = ContaBancariaRepoDominio(session=self.session)
        self.transacoes = TransacaoBancariaRepoDominio(session=self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
