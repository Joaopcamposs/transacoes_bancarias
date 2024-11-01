from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.transacao_bancaria.controllers import (
    TransacaoBancariaControllers,
)
from contextos_de_negocios.transacao_bancaria.exceptions import (
    TransacaoBancariaNaoEncontrado,
)
from contextos_de_negocios.transacao_bancaria.repositorio import (
    RepoTransacaoBancariaLeitura,
)
from contextos_de_negocios.transacao_bancaria.schemas import (
    CadastrarTransacaoBancaria,
    LerTransacaoBancaria,
)
from contextos_de_negocios.servicos.controllers import Servicos
from infra.database import get_db

router = APIRouter(
    prefix="/api/v1",
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
        transacao_bancaria = await TransacaoBancariaControllers.cadastrar(
            session=session, transacao_bancaria=novo_transacao_bancaria
        )
        return transacao_bancaria
