from fastapi import Depends, APIRouter
from pydantic import UUID4

from contextos_de_negocios.dominio.exceptions import ContaBancariaNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.conta_bancaria import (
    ContaBancariaRepoConsulta,
)
from contextos_de_negocios.dominio.entidades.conta_bancaria import (
    CadastrarContaBancaria,
    AtualizarContaBancaria,
    LerContaBancaria,
)
from contextos_de_negocios.servicos.executores.conta_bancaria import (
    cadastrar_conta,
    atualizar_conta,
    remover_conta,
)
from contextos_de_negocios.servicos.executores.seguranca import obter_usuario_atual
from libs.ddd.adaptadores.visualizadores import Filtros

router = APIRouter(
    prefix="/api",
    tags=["Conta Bancaria"],
    dependencies=[Depends(obter_usuario_atual)],
)


@router.get(
    "/conta_bancarias",
    response_model=list[LerContaBancaria],
)
async def listar(
    id: UUID4 | None = None,
    numero_da_conta: str | None = None,
    listar_transacoes: bool = False,
):
    filtros = Filtros(
        {
            "id": id,
            "numero_da_conta": numero_da_conta,
            "listar_transacoes": listar_transacoes,
        }
    )

    contas_bancarias = await ContaBancariaRepoConsulta().consultar_por_filtros(
        filtros=filtros
    )

    if not contas_bancarias:
        raise ContaBancariaNaoEncontrado

    return contas_bancarias


@router.post("/conta_bancaria", response_model=LerContaBancaria)
async def cadastrar(
    novo_conta_bancaria: CadastrarContaBancaria,
):
    conta_bancaria = await cadastrar_conta(conta_bancaria=novo_conta_bancaria)
    return conta_bancaria


@router.put("/conta_bancaria", response_model=LerContaBancaria)
async def atualizar(
    conta_bancaria_atualizado: AtualizarContaBancaria,
    id: UUID4 | None = None,
    numero_da_conta: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "numero_da_conta": numero_da_conta,
        }
    )

    conta_bancaria = await ContaBancariaRepoConsulta().consultar_um_por_filtros(
        filtros=filtros
    )

    if not conta_bancaria:
        raise ContaBancariaNaoEncontrado

    conta_bancaria_atualizado._numero_da_conta_antigo = conta_bancaria.numero_da_conta
    conta_bancaria = await atualizar_conta(
        conta_bancaria_att=conta_bancaria_atualizado,
    )
    return conta_bancaria


@router.delete("/conta_bancaria")
async def remover(
    id: UUID4 | None = None,
    numero_da_conta: str | None = None,
):
    filtros = Filtros(
        {
            "id": id,
            "numero_da_conta": numero_da_conta,
        }
    )

    conta_bancaria = await ContaBancariaRepoConsulta().consultar_um_por_filtros(
        filtros=filtros
    )

    if not conta_bancaria:
        raise ContaBancariaNaoEncontrado

    conta_bancaria_deletado = await remover_conta(id=conta_bancaria.id)
    return conta_bancaria_deletado
