from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database import DEFAULT_SQL_SESSION_FACTORY


class AbstractRepo(ABC):
    """Classe abstrata base para repositórios, definindo a interface padrão."""

    async def __aenter__(self) -> AbstractRepo:
        """Entra no contexto assíncrono do repositório."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Sai do contexto assíncrono, realizando rollback por padrão."""
        await self.rollback()

    async def commit(self) -> None:
        """Persiste as alterações no banco de dados."""
        await self._commit()

    @abstractmethod
    async def _commit(self) -> None:
        """Implementação interna do commit."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Desfaz as alterações pendentes."""
        raise NotImplementedError


class BaseDefaultRepo(AbstractRepo):
    """Repositório base padrão com gerenciamento de sessão SQLAlchemy."""

    def __init__(self, session_factory: Any = DEFAULT_SQL_SESSION_FACTORY) -> None:
        """Inicializa o repositório com a factory de sessão."""
        self.session_factory = session_factory

    async def __aenter__(self) -> BaseDefaultRepo:
        """Abre uma nova sessão assíncrona."""
        self.session: AsyncSession = self.session_factory()()
        return await super().__aenter__()

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Fecha a sessão assíncrona ao sair do contexto."""
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self) -> None:
        """Realiza o commit da sessão."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Realiza o rollback da sessão."""
        await self.session.rollback()


class DomainRepository(BaseDefaultRepo):
    """Repositório para operações de escrita no domínio."""

    ...


class QueryRepository(BaseDefaultRepo):
    """Repositório para operações de leitura/consulta."""

    ...
