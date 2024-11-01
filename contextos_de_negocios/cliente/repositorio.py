from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.cliente.exceptions import ErroAoDeletarCliente
from contextos_de_negocios.cliente.models import Cliente
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class RepoClienteLeitura:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[Cliente]:
        clientes = (await session.execute(select(Cliente))).scalars().all()
        return clientes

    @staticmethod
    async def consultar_por_id(session: AsyncSession, id: Uuid) -> Cliente | None:
        cliente = await session.get(Cliente, id)
        return cliente

    @staticmethod
    async def consultar_por_cpf(session: AsyncSession, cpf: str) -> Cliente | None:
        cliente = (
            await session.execute(select(Cliente).filter_by(cpf=cpf))
        ).scalar_one_or_none()
        return cliente


class RepoClienteEscrita:
    @staticmethod
    async def adicionar(
        session: AsyncSession,
        cliente: Cliente,
        tipo_operacao: TipoOperacao,
    ) -> Cliente:
        if tipo_operacao == TipoOperacao.INSERCAO:
            try:
                session.add(cliente)
                await session.commit()
                await session.refresh(cliente)
            except Exception as erro:
                await session.rollback()
                raise erro
        elif tipo_operacao == TipoOperacao.ATUALIZACAO:
            try:
                await session.merge(cliente)
                await session.commit()
                await session.refresh(cliente)
            except Exception as erro:
                await session.rollback()
                raise erro
        return cliente

    @staticmethod
    async def remover(session: AsyncSession, cliente: Cliente) -> None:
        try:
            await session.delete(cliente)
            await session.commit()
        except Exception as erro:
            await session.rollback()
            raise ErroAoDeletarCliente(
                detail=f"Erro ao deletar cliente: {erro}",
            )
