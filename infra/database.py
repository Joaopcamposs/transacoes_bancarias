from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from contextos_de_negocios.utils.constantes import (
    SENHA_PRIMEIRO_USUARIO,
    EMAIL_PRIMEIRO_USUARIO,
    SQLITE_TESTE,
    DB_HOST,
    DB_PASSWORD,
    DB_USER,
    DB_NAME,
)


def obter_uri_do_banco_de_dados(eh_teste: bool = False) -> str:
    if eh_teste:
        return SQLITE_TESTE

    host = DB_HOST
    port = 54321 if host == "localhost" and not eh_teste else 5432
    password = DB_PASSWORD
    user = DB_USER
    db_name = DB_NAME
    database_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    return database_uri


Base = declarative_base()

engine = create_async_engine(
    obter_uri_do_banco_de_dados(),
    isolation_level="REPEATABLE READ",  # usar 'REPEATABLE READ' quando postgres, SERIALIZABLE para sqlite
    future=True,
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def extrair_sessao(conexao: AsyncIterable = get_db()) -> AsyncSession:
    async for session in conexao:
        return session


async def criar_primeiro_usuario() -> None:
    from contextos_de_negocios.repositorio.repo_consulta.usuario import (
        UsuarioRepoConsulta,
    )
    from contextos_de_negocios.dominio.entidades.usuario import (
        CadastrarEAtualizarUsuario,
    )
    from contextos_de_negocios.servicos.executores.usuario import UsuarioControllers

    async with SessionLocal() as session:
        usuarios = await UsuarioRepoConsulta.consultar_todos(session=session)
        if not usuarios:
            usuario = CadastrarEAtualizarUsuario(
                nome="Admin",
                email=EMAIL_PRIMEIRO_USUARIO,
                senha=SENHA_PRIMEIRO_USUARIO,
                adm=True,
                ativo=True,
            )
            await UsuarioControllers.cadastrar(session=session, usuario=usuario)
