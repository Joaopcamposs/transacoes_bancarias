from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.servicos.executores.conta_bancaria import (
    ContaBancariaControllers,
)
from contextos_de_negocios.dominio.exceptions import ContaBancariaNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.conta_bancaria import (
    ContaBancariaRepoConsulta,
)
from contextos_de_negocios.dominio.entidades.conta_bancaria import (
    CadastrarContaBancaria,
    AtualizarContaBancaria,
    LerContaBancaria,
    LerContaBancariaETransacoes,
)
from contextos_de_negocios.servicos.executores.seguranca import Servicos
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    LerTransacaoBancaria,
)
from infra.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Conta Bancaria"],
    dependencies=[Depends(Servicos.obter_usuario_atual)],
)


class ContaBancariaRoutes:
    @staticmethod
    @router.get(
        "/conta_bancarias",
        response_model=list[LerContaBancaria] | LerContaBancariaETransacoes,
    )
    async def consultar_conta_bancarias(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        numero_da_conta: str | None = None,
        listar_transacoes: bool = False,
    ):
        if id:
            conta_bancarias = [
                await ContaBancariaRepoConsulta.consultar_por_id(session=session, id=id)
            ]
        elif numero_da_conta:
            conta_bancarias = [
                await ContaBancariaRepoConsulta.consultar_por_numero_da_conta(
                    session=session, numero_da_conta=numero_da_conta
                )
            ]
        else:
            conta_bancarias = await ContaBancariaRepoConsulta.consultar_todos(
                session=session
            )

        if not conta_bancarias or conta_bancarias == [None]:
            raise ContaBancariaNaoEncontrado

        if listar_transacoes:
            return LerContaBancariaETransacoes(
                contas=[
                    LerContaBancaria.from_conta(conta) for conta in conta_bancarias
                ],
                transacoes=[
                    LerTransacaoBancaria.from_transacao(transacao)
                    for conta in conta_bancarias
                    for transacao in conta.transacoes
                ],
            )

        return conta_bancarias

    @staticmethod
    @router.post("/conta_bancaria", response_model=LerContaBancaria)
    async def cadastrar_conta_bancaria(
        novo_conta_bancaria: CadastrarContaBancaria,
        session: AsyncSession = Depends(get_db),
    ):
        conta_bancaria = await ContaBancariaControllers.cadastrar(
            session=session, conta_bancaria=novo_conta_bancaria
        )
        return conta_bancaria

    @staticmethod
    @router.put("/conta_bancaria", response_model=LerContaBancaria)
    async def atualizar_conta_bancaria(
        conta_bancaria_atualizado: AtualizarContaBancaria,
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        numero_da_conta: str | None = None,
    ):
        if id:
            conta_bancaria = await ContaBancariaRepoConsulta.consultar_por_id(
                session=session, id=id
            )
        else:
            conta_bancaria = (
                await ContaBancariaRepoConsulta.consultar_por_numero_da_conta(
                    session=session, numero_da_conta=numero_da_conta
                )
            )

        if not conta_bancaria:
            raise ContaBancariaNaoEncontrado

        conta_bancaria = await ContaBancariaControllers.atualizar_por_id(
            session=session,
            id=conta_bancaria.id,
            conta_bancaria_att=conta_bancaria_atualizado,
        )
        return conta_bancaria

    @staticmethod
    @router.delete("/conta_bancaria")
    async def deletar_conta_bancaria(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        numero_da_conta: str | None = None,
    ):
        if id:
            conta_bancaria = await ContaBancariaRepoConsulta.consultar_por_id(
                session=session, id=id
            )
        else:
            conta_bancaria = (
                await ContaBancariaRepoConsulta.consultar_por_numero_da_conta(
                    session=session, numero_da_conta=numero_da_conta
                )
            )

        if not conta_bancaria:
            raise ContaBancariaNaoEncontrado

        conta_bancaria_deletado = await ContaBancariaControllers.deletar_por_id(
            session=session, id=conta_bancaria.id
        )
        return conta_bancaria_deletado
