from fastapi import Depends, APIRouter
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.servicos.executores.cliente import ClienteControllers
from contextos_de_negocios.dominio.exceptions import (
    ClienteNaoEncontrado,
)
from contextos_de_negocios.repositorio.repo_consulta.cliente import RepoClienteLeitura
from contextos_de_negocios.dominio.entidades.cliente import (
    CadastrarEAtualizarCliente,
    LerCliente,
)
from contextos_de_negocios.servicos.executores.seguranca import Servicos
from infra.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Clientes"],
    dependencies=[Depends(Servicos.obter_usuario_atual)],
)


class ClienteRoutes:
    @staticmethod
    @router.get("/clientes", response_model=list[LerCliente])
    async def consultar_clientes(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        cpf: str | None = None,
    ):
        if id:
            clientes = [
                await RepoClienteLeitura.consultar_por_id(session=session, id=id)
            ]
        elif cpf:
            clientes = [
                await RepoClienteLeitura.consultar_por_cpf(session=session, cpf=cpf)
            ]
        else:
            clientes = await RepoClienteLeitura.consultar_todos(session=session)

        if not clientes or clientes == [None]:
            raise ClienteNaoEncontrado

        return clientes

    @staticmethod
    @router.post("/cliente", response_model=LerCliente)
    async def cadastrar_cliente(
        novo_cliente: CadastrarEAtualizarCliente,
        session: AsyncSession = Depends(get_db),
    ):
        cliente = await ClienteControllers.cadastrar(
            session=session, cliente=novo_cliente
        )
        return cliente

    @staticmethod
    @router.put("/cliente", response_model=LerCliente)
    async def atualizar_cliente(
        cliente_atualizado: CadastrarEAtualizarCliente,
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        cpf: str | None = None,
    ):
        if id:
            cliente = await RepoClienteLeitura.consultar_por_id(session=session, id=id)
        else:
            cliente = await RepoClienteLeitura.consultar_por_cpf(
                session=session, cpf=cpf
            )

        if not cliente:
            raise ClienteNaoEncontrado

        cliente = await ClienteControllers.atualizar_por_id(
            session=session, id=cliente.id, cliente_att=cliente_atualizado
        )
        return cliente

    @staticmethod
    @router.delete("/cliente")
    async def deletar_cliente(
        session: AsyncSession = Depends(get_db),
        id: UUID4 | None = None,
        cpf: str | None = None,
    ):
        if id:
            cliente = await RepoClienteLeitura.consultar_por_id(session=session, id=id)
        else:
            cliente = await RepoClienteLeitura.consultar_por_cpf(
                session=session, cpf=cpf
            )

        if not cliente:
            raise ClienteNaoEncontrado

        cliente_deletado = await ClienteControllers.deletar_por_id(
            session=session, id=cliente.id
        )
        return cliente_deletado
