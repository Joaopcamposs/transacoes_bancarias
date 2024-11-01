from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.servicos.controllers import Servicos
from contextos_de_negocios.usuario.controllers import UsuarioControllers
from contextos_de_negocios.usuario.exceptions import (
    UsuarioNaoEncontrado,
)
from contextos_de_negocios.usuario.repositorio import RepoUsuarioLeitura
from contextos_de_negocios.usuario.schemas import CadastrarEAtualizarUsuario, LerUsuario
from infra.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Usuarios"],
    dependencies=[Depends(Servicos.obter_usuario_atual_adm)],
)


class UsuarioRoutes:
    @staticmethod
    @router.get("/usuarios", response_model=list[LerUsuario])
    async def consultar_usuarios(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        email: str | None = None,
    ):
        if id:
            usuarios = [
                await RepoUsuarioLeitura.consultar_por_id(session=session, id=id)
            ]
        elif email:
            usuarios = [
                await RepoUsuarioLeitura.consultar_por_email(
                    session=session, email=email
                )
            ]
        else:
            usuarios = await RepoUsuarioLeitura.consultar_todos(session=session)

        if not usuarios or usuarios == [None]:
            raise UsuarioNaoEncontrado

        return usuarios

    @staticmethod
    @router.post("/usuario", response_model=LerUsuario)
    async def cadastrar_usuario(
        novo_usuario: CadastrarEAtualizarUsuario,
        session: AsyncSession = Depends(get_db),
    ):
        usuario = await UsuarioControllers.cadastrar(
            session=session, usuario=novo_usuario
        )
        return usuario

    @staticmethod
    @router.put("/usuario", response_model=LerUsuario)
    async def atualizar_usuario(
        usuario_atualizado: CadastrarEAtualizarUsuario,
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        email: str | None = None,
    ):
        if id:
            usuario = await RepoUsuarioLeitura.consultar_por_id(session=session, id=id)
        else:
            usuario = await RepoUsuarioLeitura.consultar_por_email(
                session=session, email=email
            )

        if not usuario:
            raise UsuarioNaoEncontrado

        usuario = await UsuarioControllers.atualizar_por_id(
            session=session, id=usuario.id, usuario_att=usuario_atualizado
        )
        return usuario

    @staticmethod
    @router.delete("/usuario")
    async def deletar_usuario(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        email: str | None = None,
    ):
        if id:
            usuario = await RepoUsuarioLeitura.consultar_por_id(session=session, id=id)
        else:
            usuario = await RepoUsuarioLeitura.consultar_por_email(
                session=session, email=email
            )

        if not usuario:
            raise UsuarioNaoEncontrado

        usuario_deletado = await UsuarioControllers.deletar_por_id(
            session=session, id=usuario.id
        )
        return usuario_deletado
