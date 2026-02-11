import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, registry

from business_contexts.utils.constants import (
    FIRST_USER_PASSWORD,
    FIRST_USER_EMAIL,
    DB_HOST,
    DB_PASSWORD,
    DB_USER,
    DB_NAME,
    DB_PORT,
)
from libs.ddd.adapters.viewers import Filters

mapper_registry: registry = registry()


def get_database_uri() -> str:
    """Retorna a URI de conexão PostgreSQL com o banco de dados."""
    host: str = os.getenv("DB_HOST", DB_HOST)
    port: int = int(os.getenv("DB_PORT", str(DB_PORT)))
    password: str = os.getenv("DB_PASSWORD", DB_PASSWORD)
    user: str = os.getenv("DB_USER", DB_USER)
    db_name: str = os.getenv("DB_NAME", DB_NAME)
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


async def create_first_user() -> None:
    """Cria o primeiro usuário administrador caso não exista nenhum usuário cadastrado."""
    from business_contexts.repository.query_repo.user import UserQueryRepo
    from business_contexts.domain.entities.user import CreateUser
    from business_contexts.services.executors.user import create_user

    users = await UserQueryRepo().query_by_filters(Filters({}))
    if not users:
        user = CreateUser(
            name="Admin",
            email=FIRST_USER_EMAIL,
            password=FIRST_USER_PASSWORD,
            is_admin=True,
            is_active=True,
        )
        await create_user(user=user)


ASYNC_ENGINE: AsyncEngine | None = None


def get_async_engine() -> AsyncEngine:
    """Retorna a engine assíncrona do SQLAlchemy (PostgreSQL), criando-a se necessário."""
    global ASYNC_ENGINE

    if not ASYNC_ENGINE:
        ASYNC_ENGINE = create_async_engine(
            get_database_uri(),
            isolation_level="REPEATABLE READ",
            future=True,
        )

    return ASYNC_ENGINE


def reset_engine() -> None:
    """Reseta a engine global. Usado para testes que precisam trocar a URI."""
    global ASYNC_ENGINE
    ASYNC_ENGINE = None


def DEFAULT_SQL_SESSION_FACTORY() -> sessionmaker[AsyncSession]:
    """Retorna a factory de sessão SQL assíncrona padrão."""
    _engine: AsyncEngine = get_async_engine()

    async_session: sessionmaker[AsyncSession] = sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    return async_session
