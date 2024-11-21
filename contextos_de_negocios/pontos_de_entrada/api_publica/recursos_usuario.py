from fastapi import Depends, APIRouter
from pydantic import UUID4

from contextos_de_negocios.dominio.exceptions import UsuarioNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.usuario import UsuarioRepoConsulta
from contextos_de_negocios.dominio.entidades.usuario import (
    CadastrarUsuario,
    LerUsuario,
    AtualizarUsuario,
)
from contextos_de_negocios.servicos.executores.seguranca import obter_usuario_atual_adm
from contextos_de_negocios.servicos.executores.usuario import (
    remover_usuario,
    cadastrar_usuario,
    atualizar_usuario,
)
from libs.ddd.adaptadores.visualizadores import Filtros

router = APIRouter(
    prefix="/api",
    tags=["Usuarios"],
    dependencies=[Depends(obter_usuario_atual_adm)],
)


@router.get("/usuarios", response_model=list[LerUsuario])
async def listar(
    id: UUID4 | None = None,
    email: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "email": email,
        }
    )

    usuarios = await UsuarioRepoConsulta().consultar_por_filtros(filtros=filtros)

    if not usuarios:
        raise UsuarioNaoEncontrado

    return usuarios


@router.post("/usuario", response_model=LerUsuario)
async def cadastrar(
    novo_usuario: CadastrarUsuario,
):
    usuario = await cadastrar_usuario(usuario=novo_usuario)
    return usuario


@router.put("/usuario", response_model=LerUsuario)
async def atualizar(
    usuario_atualizado: AtualizarUsuario,
    id: UUID4 | None = None,
    email: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "email": email,
        }
    )

    usuario = await UsuarioRepoConsulta().consultar_um_por_filtros(filtros=filtros)

    if not usuario:
        raise UsuarioNaoEncontrado

    usuario_atualizado._id = usuario.id
    usuario = await atualizar_usuario(usuario_att=usuario_atualizado)
    return usuario


@router.delete("/usuario")
async def remover(
    id: UUID4 | None = None,
    email: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "email": email,
        }
    )

    usuario = await UsuarioRepoConsulta().consultar_um_por_filtros(filtros=filtros)

    if not usuario:
        raise UsuarioNaoEncontrado

    usuario_deletado = await remover_usuario(id=usuario.id)
    return usuario_deletado
