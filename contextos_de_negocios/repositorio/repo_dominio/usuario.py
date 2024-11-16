from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.repositorio.orm.usuario import Usuario
from contextos_de_negocios.dominio.exceptions import ErroAoDeletarUsuario
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class UsuarioRepoDominio:
    @staticmethod
    async def adicionar(
        session: AsyncSession,
        usuario: Usuario,
        tipo_operacao: TipoOperacao,
    ) -> Usuario:
        if tipo_operacao == TipoOperacao.INSERCAO:
            try:
                session.add(usuario)
                await session.commit()
                await session.refresh(usuario)
            except Exception as erro:
                await session.rollback()
                raise erro
        elif tipo_operacao == TipoOperacao.ATUALIZACAO:
            try:
                await session.merge(usuario)
                await session.commit()
                await session.refresh(usuario)
            except Exception as erro:
                await session.rollback()
                raise erro
        return usuario

    @staticmethod
    async def remover(session: AsyncSession, usuario: Usuario) -> None:
        try:
            await session.delete(usuario)
            await session.commit()
        except Exception as erro:
            await session.rollback()
            raise ErroAoDeletarUsuario(
                detail=f"Erro ao deletar usuário: {erro}",
            )
