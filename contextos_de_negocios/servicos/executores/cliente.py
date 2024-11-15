from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.exceptions import (
    ClienteJaCadastrado,
    ClienteNaoEncontrado,
    ErroAoDeletarCliente,
    ErroAoAtualizarCliente,
    ErroAoCadastrarCliente,
)
from contextos_de_negocios.repositorio.orm.cliente import Cliente
from contextos_de_negocios.repositorio.repo_consulta.cliente import (
    RepoClienteLeitura,
)
from contextos_de_negocios.repositorio.repo_dominio.cliente import RepoClienteEscrita
from contextos_de_negocios.dominio.entidades.cliente import CadastrarEAtualizarCliente
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao, CPF


class ClienteControllers:
    @staticmethod
    async def cadastrar(
        session: AsyncSession,
        cliente: CadastrarEAtualizarCliente,
    ) -> Cliente:
        CPF(cliente.cpf)

        cliente_no_banco = await RepoClienteLeitura.consultar_por_cpf(
            session=session, cpf=cliente.cpf
        )

        if cliente_no_banco:
            raise ClienteJaCadastrado

        novo_cliente = Cliente(**cliente.dict())
        try:
            novo_cliente = await RepoClienteEscrita.adicionar(
                session=session,
                cliente=novo_cliente,
                tipo_operacao=TipoOperacao.INSERCAO,
            )
        except Exception as erro:
            raise ErroAoCadastrarCliente(
                detail=f"Erro ao cadastrar usuário: {erro}",
            )
        return novo_cliente

    @staticmethod
    async def atualizar_por_id(
        session: AsyncSession, id: Uuid, cliente_att: CadastrarEAtualizarCliente
    ) -> Cliente:
        CPF(cliente_att.cpf)

        cliente = await RepoClienteLeitura.consultar_por_id(session=session, id=id)

        if not cliente:
            raise ClienteNaoEncontrado

        for atributo, valor in cliente_att.dict().items():
            setattr(cliente, atributo, valor)

        try:
            cliente = await RepoClienteEscrita.adicionar(
                session=session, cliente=cliente, tipo_operacao=TipoOperacao.ATUALIZACAO
            )
        except Exception as erro:
            raise ErroAoAtualizarCliente(
                detail=f"Erro ao atualizar cliente: {erro}",
            )
        return cliente

    @staticmethod
    async def deletar_por_id(session: AsyncSession, id: Uuid) -> str:
        cliente = await RepoClienteLeitura.consultar_por_id(session=session, id=id)

        if not cliente:
            raise ClienteNaoEncontrado

        try:
            await RepoClienteEscrita.remover(session=session, cliente=cliente)
        except Exception as erro:
            raise ErroAoDeletarCliente(
                detail=f"Erro ao deletar cliente: {erro}",
            )

        return "Cliente deletado!"
