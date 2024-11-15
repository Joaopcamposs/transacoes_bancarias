from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.servicos.executores.transacao_bancaria import (
    cadastrar_transacao_bancaria,
)
from contextos_de_negocios.dominio.exceptions import TransacaoBancariaNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.transacao_bancaria import (
    RepoTransacaoBancariaLeitura,
)
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
    LerTransacaoBancaria,
)
from contextos_de_negocios.servicos.executores.seguranca import Servicos
from infra.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Transacao Bancaria"],
    dependencies=[Depends(Servicos.obter_usuario_atual)],
)


class TransacaoBancariaRoutes:
    @staticmethod
    @router.get("/transacao_bancarias", response_model=list[LerTransacaoBancaria])
    async def consultar_transacao_bancarias(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
    ):
        if id:
            transacao_bancarias = [
                await RepoTransacaoBancariaLeitura.consultar_por_id(
                    session=session, id=id
                )
            ]
        else:
            transacao_bancarias = await RepoTransacaoBancariaLeitura.consultar_todos(
                session=session
            )

        if not transacao_bancarias or transacao_bancarias == [None]:
            raise TransacaoBancariaNaoEncontrado

        return transacao_bancarias

    @staticmethod
    @router.post("/transacao_bancaria", response_model=LerTransacaoBancaria)
    async def cadastrar_transacao_bancaria(
        novo_transacao_bancaria: CadastrarTransacaoBancaria,
        session: AsyncSession = Depends(get_db),
    ):
        transacao_bancaria = await cadastrar_transacao_bancaria(
            session=session, transacao_bancaria=novo_transacao_bancaria
        )
        return transacao_bancaria
