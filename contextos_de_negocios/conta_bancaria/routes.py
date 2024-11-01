from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.conta_bancaria.controllers import ContaBancariaControllers
from contextos_de_negocios.conta_bancaria.exceptions import (
    ContaBancariaNaoEncontrado,
)
from contextos_de_negocios.conta_bancaria.repositorio import RepoContaBancariaLeitura
from contextos_de_negocios.conta_bancaria.schemas import (
    CadastrarContaBancaria,
    AtualizarContaBancaria,
    LerContaBancaria,
)
from contextos_de_negocios.servicos.controllers import Servicos
from infra.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Conta Bancaria"],
    dependencies=[Depends(Servicos.obter_usuario_atual)],
)


class ContaBancariaRoutes:
    @staticmethod
    @router.get("/conta_bancarias", response_model=list[LerContaBancaria])
    async def consultar_conta_bancarias(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        numero_da_conta: str | None = None,
    ):
        if id:
            conta_bancarias = [
                await RepoContaBancariaLeitura.consultar_por_id(session=session, id=id)
            ]
        elif numero_da_conta:
            conta_bancarias = [
                await RepoContaBancariaLeitura.consultar_por_numero_da_conta(
                    session=session, numero_da_conta=numero_da_conta
                )
            ]
        else:
            conta_bancarias = await RepoContaBancariaLeitura.consultar_todos(
                session=session
            )

        if not conta_bancarias or conta_bancarias == [None]:
            raise ContaBancariaNaoEncontrado

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
            conta_bancaria = await RepoContaBancariaLeitura.consultar_por_id(
                session=session, id=id
            )
        else:
            conta_bancaria = (
                await RepoContaBancariaLeitura.consultar_por_numero_da_conta(
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
            conta_bancaria = await RepoContaBancariaLeitura.consultar_por_id(
                session=session, id=id
            )
        else:
            conta_bancaria = (
                await RepoContaBancariaLeitura.consultar_por_numero_da_conta(
                    session=session, numero_da_conta=numero_da_conta
                )
            )

        if not conta_bancaria:
            raise ContaBancariaNaoEncontrado

        conta_bancaria_deletado = await ContaBancariaControllers.deletar_por_id(
            session=session, id=conta_bancaria.id
        )
        return conta_bancaria_deletado
