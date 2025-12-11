import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, registry, declarative_base

from contextos_de_negocios.utils.constantes import (
    SENHA_PRIMEIRO_USUARIO,
    EMAIL_PRIMEIRO_USUARIO,
    DB_HOST,
    DB_PASSWORD,
    DB_USER,
    DB_NAME,
)
from libs.ddd.adaptadores.visualizadores import Filtros


def obter_uri_do_banco_de_dados(eh_teste: bool = False) -> str:
    from contextos_de_negocios.utils.constantes import POSTGRES_TESTE

    if eh_teste or os.getenv("TEST_ENV", "false").lower() == "true":
        return POSTGRES_TESTE

    host = DB_HOST
    port = 54321 if host == "localhost" and not eh_teste else 5432
    password = DB_PASSWORD
    user = DB_USER
    db_name = DB_NAME
    database_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    return database_uri


mapper_registry = registry()
Base = declarative_base()


async def criar_primeiro_usuario() -> None:
    from contextos_de_negocios.repositorio.repo_consulta.usuario import (
        UsuarioRepoConsulta,
    )
    from contextos_de_negocios.dominio.entidades.usuario import (
        CadastrarUsuario,
    )
    from contextos_de_negocios.servicos.executores.usuario import cadastrar_usuario
    from sqlalchemy.exc import IntegrityError

    usuarios = await UsuarioRepoConsulta().consultar_por_filtros(Filtros({}))
    if not usuarios:
        usuario = CadastrarUsuario(
            nome="Admin",
            email=EMAIL_PRIMEIRO_USUARIO,
            senha=SENHA_PRIMEIRO_USUARIO,
            adm=True,
            ativo=True,
        )
        try:
            await cadastrar_usuario(usuario=usuario)
        except IntegrityError:
            # Usuário já foi criado por outra thread/processo concorrente
            pass


ASYNC_ENGINE: AsyncEngine | None = None


def obter_async_engine() -> AsyncEngine:
    def _criar_engine_correta() -> AsyncEngine:
        global ASYNC_ENGINE

        if not ASYNC_ENGINE:
            url_banco_de_dados = obter_uri_do_banco_de_dados()
            if "sqlite" in url_banco_de_dados:
                ASYNC_ENGINE = create_async_engine(
                    url_banco_de_dados,
                    future=True,
                    isolation_level="SERIALIZABLE",
                )
                return ASYNC_ENGINE
            ASYNC_ENGINE = create_async_engine(
                url_banco_de_dados,
                isolation_level="REPEATABLE READ",
                future=True,
            )

        return ASYNC_ENGINE

    engine_correta = _criar_engine_correta()

    return engine_correta


def DEFAULT_SQL_SESSION_FACTORY() -> sessionmaker[AsyncSession]:
    _engine = obter_async_engine()

    async_session = sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    return async_session
