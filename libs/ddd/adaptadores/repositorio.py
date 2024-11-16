from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class Repositorio(ABC):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session


class RepositorioDominio(Repositorio):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.session = session


class RepositorioConsulta(Repositorio):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.session = session
        self.somente_leitura = True
