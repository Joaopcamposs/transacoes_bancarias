from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from contextos_de_negocios.utils.constantes import SQLITE_TESTE
from infra.database import Base

override_engine = create_async_engine(
    url=SQLITE_TESTE,
    isolation_level="SERIALIZABLE",
    future=True,
)
SessionLocalTestes = sessionmaker(
    bind=override_engine, expire_on_commit=False, class_=AsyncSession
)


async def override_get_db():
    async with override_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocalTestes() as session:
        yield session
