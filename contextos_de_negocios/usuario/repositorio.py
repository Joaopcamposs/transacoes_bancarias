from typing import Sequence

from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.usuario.exceptions import ErroAoDeletarUsuario
from contextos_de_negocios.usuario.models import Usuario
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class RepoUsuarioLeitura:
    @staticmethod
    async def consultar_todos(session: AsyncSession) -> Sequence[Usuario]:
        usuarios = (await session.execute(select(Usuario))).scalars().all()
        return usuarios

    @staticmethod
    async def consultar_por_id(session: AsyncSession, id: Uuid) -> Usuario | None:
        usuario = await session.get(Usuario, id)
        return usuario

    @staticmethod
    async def consultar_por_email(session: AsyncSession, email: str) -> Usuario | None:
        usuario = (
            await session.execute(select(Usuario).filter_by(email=email.lower()))
        ).scalar_one_or_none()
        return usuario


class RepoUsuarioEscrita:
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
