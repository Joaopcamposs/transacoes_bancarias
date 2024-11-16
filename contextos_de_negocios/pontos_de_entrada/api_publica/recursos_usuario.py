from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.servicos.executores.seguranca import Seguranca
from contextos_de_negocios.dominio.exceptions import UsuarioNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.usuario import UsuarioRepoConsulta
from contextos_de_negocios.dominio.entidades.usuario import (
    CadastrarUsuario,
    LerUsuario,
    AtualizarUsuario,
)
from contextos_de_negocios.servicos.executores.usuario import (
    remover_usuario,
    cadastrar_usuario,
    atualizar_usuario,
)
from infra.database import get_db
from libs.ddd.adaptadores.visualizadores import Filtros

router = APIRouter(
    prefix="/api",
    tags=["Usuarios"],
    dependencies=[Depends(Seguranca.obter_usuario_atual_adm)],
)


@router.get("/usuarios", response_model=list[LerUsuario])
async def listar(
    session: AsyncSession = Depends(get_db),
    id: UUID4 | None = None,
    email: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "email": email,
        }
    )

    usuarios = await UsuarioRepoConsulta(session=session).consultar_por_filtros(
        filtros=filtros
    )

    if not usuarios:
        raise UsuarioNaoEncontrado

    return usuarios


@router.post("/usuario", response_model=LerUsuario)
async def cadastrar(
    novo_usuario: CadastrarUsuario,
    session: AsyncSession = Depends(get_db),
):
    usuario = await cadastrar_usuario(session=session, usuario=novo_usuario)
    return usuario


@router.put("/usuario", response_model=LerUsuario)
async def atualizar(
    usuario_atualizado: AtualizarUsuario,
    session: AsyncSession = Depends(get_db),
    id: UUID4 | None = None,
    email: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "email": email,
        }
    )

    usuario = await UsuarioRepoConsulta(session=session).consultar_um_por_filtros(
        filtros=filtros
    )

    if not usuario:
        raise UsuarioNaoEncontrado

    usuario_atualizado._id = usuario.id
    usuario = await atualizar_usuario(session=session, usuario_att=usuario_atualizado)
    return usuario


@router.delete("/usuario")
async def remover(
    session: AsyncSession = Depends(get_db),
    id: UUID4 | None = None,
    email: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "email": email,
        }
    )

    usuario = await UsuarioRepoConsulta(session=session).consultar_um_por_filtros(
        filtros=filtros
    )

    if not usuario:
        raise UsuarioNaoEncontrado

    usuario_deletado = await remover_usuario(session=session, id=usuario.id)
    return usuario_deletado
