from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from contextos_de_negocios.utils.constantes import (
    DATABASE_URI,
    SENHA_PRIMEIRO_USUARIO,
)

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URI,
    isolation_level="SERIALIZABLE",  # usar 'REPEATABLE READ' quando postgres real, SERIALIZABLE para sqlite
    future=True,
    echo=True,
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def extrair_sessao():
    async for session in get_db():
        return session


async def criar_primeiro_usuario() -> None:
    from contextos_de_negocios.usuario.repositorio import RepoUsuarioLeitura
    from contextos_de_negocios.usuario.schemas import CadastrarEAtualizarUsuario
    from contextos_de_negocios.usuario.controllers import UsuarioControllers

    async with SessionLocal() as session:
        usuarios = await RepoUsuarioLeitura.consultar_todos(session=session)
        if not usuarios:
            usuario = CadastrarEAtualizarUsuario(
                nome="Admin",
                email="admin@email.com",
                senha=SENHA_PRIMEIRO_USUARIO,
                adm=True,
                ativo=True,
            )
            await UsuarioControllers.cadastrar(session=session, usuario=usuario)
