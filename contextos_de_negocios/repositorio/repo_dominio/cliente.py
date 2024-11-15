from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.exceptions import ErroAoDeletarCliente
from contextos_de_negocios.repositorio.orm.cliente import Cliente
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


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
