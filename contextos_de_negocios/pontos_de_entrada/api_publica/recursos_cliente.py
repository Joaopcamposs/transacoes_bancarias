from fastapi import Depends, APIRouter
from pydantic import UUID4

from contextos_de_negocios.dominio.exceptions import (
    ClienteNaoEncontrado,
)
from contextos_de_negocios.repositorio.repo_consulta.cliente import ClienteRepoConsulta
from contextos_de_negocios.dominio.entidades.cliente import (
    CadastrarCliente,
    LerCliente,
    AtualizarCliente,
)
from contextos_de_negocios.servicos.executores.cliente import (
    cadastrar_cliente,
    atualizar_cliente,
    remover_cliente,
)
from contextos_de_negocios.servicos.executores.seguranca import obter_usuario_atual
from libs.ddd.adaptadores.visualizadores import Filtros

router = APIRouter(
    prefix="/api",
    tags=["Clientes"],
    dependencies=[Depends(obter_usuario_atual)],
)


@router.get("/clientes", response_model=list[LerCliente])
async def listar(
    id: UUID4 | None = None,
    cpf: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "cpf": cpf,
        }
    )

    clientes = await ClienteRepoConsulta().consultar_por_filtros(filtros=filtros)

    if not clientes:
        raise ClienteNaoEncontrado

    return clientes


@router.post("/cliente", response_model=LerCliente)
async def cadastrar(
    novo_cliente: CadastrarCliente,
):
    cliente = await cadastrar_cliente(cliente=novo_cliente)
    return cliente


@router.put("/cliente", response_model=LerCliente)
async def atualizar(
    cliente_atualizado: AtualizarCliente,
    id: UUID4 | None = None,
    cpf: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "cpf": cpf,
        }
    )

    cliente = await ClienteRepoConsulta().consultar_um_por_filtros(filtros=filtros)

    if not cliente:
        raise ClienteNaoEncontrado

    cliente_atualizado._id = cliente.id
    cliente = await atualizar_cliente(cliente_att=cliente_atualizado)
    return cliente


@router.delete("/cliente")
async def remover(
    id: UUID4 | None = None,
    cpf: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "cpf": cpf,
        }
    )

    cliente = await ClienteRepoConsulta().consultar_um_por_filtros(filtros=filtros)

    if not cliente:
        raise ClienteNaoEncontrado

    cliente_deletado = await remover_cliente(id=cliente.id)
    return cliente_deletado
