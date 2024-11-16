from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.servicos.executores.transacao_bancaria import (
    cadastrar_transacao_bancaria,
)
from contextos_de_negocios.dominio.exceptions import TransacaoBancariaNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.transacao_bancaria import (
    TransacaoBancariaRepoConsulta,
)
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
    LerTransacaoBancaria,
)
from contextos_de_negocios.servicos.executores.seguranca import Seguranca
from infra.database import get_db
from libs.ddd.adaptadores.visualizadores import Filtros

router = APIRouter(
    prefix="/api",
    tags=["Transacao Bancaria"],
    dependencies=[Depends(Seguranca.obter_usuario_atual)],
)


@router.get("/transacao_bancarias", response_model=list[LerTransacaoBancaria])
async def listar(
    session: AsyncSession = Depends(get_db),
    id: UUID4 | None = None,
    # todo adicionar busca por numero da conta
):
    filtros = Filtros(
        {
            "id": id,
        }
    )

    transacoes = await TransacaoBancariaRepoConsulta(
        session=session
    ).consultar_por_filtros(filtros=filtros)

    if not transacoes:
        raise TransacaoBancariaNaoEncontrado

    return transacoes


@router.post("/transacao_bancaria", response_model=LerTransacaoBancaria)
async def cadastrar(
    novo_transacao_bancaria: CadastrarTransacaoBancaria,
    session: AsyncSession = Depends(get_db),
):
    transacao_bancaria = await cadastrar_transacao_bancaria(
        session=session, transacao_bancaria=novo_transacao_bancaria
    )
    return transacao_bancaria
