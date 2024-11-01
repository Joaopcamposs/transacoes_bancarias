from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from contextos_de_negocios.usuario.exceptions import (
    UsuarioJaCadastrado,
    UsuarioNaoEncontrado,
)
from contextos_de_negocios.usuario.models import Usuario
from contextos_de_negocios.usuario.repositorio import (
    RepoUsuarioLeitura,
    RepoUsuarioEscrita,
)
from contextos_de_negocios.usuario.schemas import CadastrarEAtualizarUsuario
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class UsuarioControllers:
    @staticmethod
    async def cadastrar(
        session: AsyncSession,
        usuario: CadastrarEAtualizarUsuario,
        criptografar_senha: bool = True,
    ) -> Usuario:
        from contextos_de_negocios.servicos.controllers import Servicos

        usuario_no_banco = await RepoUsuarioLeitura.consultar_por_email(
            session=session, email=usuario.email
        )

        if usuario_no_banco:
            raise UsuarioJaCadastrado

        novo_usuario = Usuario(**usuario.dict())
        novo_usuario.email = novo_usuario.email.lower()
        if criptografar_senha:
            novo_usuario.senha = Servicos.criptografar_senha(novo_usuario.senha)

        try:
            novo_usuario = await RepoUsuarioEscrita.adicionar(
                session=session,
                usuario=novo_usuario,
                tipo_operacao=TipoOperacao.INSERCAO,
            )
        except Exception as erro:
            raise HTTPException(
                detail=f"Erro ao cadastrar usuário: {erro}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return novo_usuario

    @staticmethod
    async def atualizar_por_id(
        session: AsyncSession, id: Uuid, usuario_att: CadastrarEAtualizarUsuario
    ) -> Usuario:
        from contextos_de_negocios.servicos.controllers import Servicos

        usuario = await RepoUsuarioLeitura.consultar_por_id(session=session, id=id)

        if not usuario:
            raise UsuarioNaoEncontrado

        usuario_att.email = usuario_att.email.lower()
        usuario_att.senha = Servicos.criptografar_senha(usuario_att.senha)

        # Atualiza os dados do acessório
        for atributo, valor in usuario_att.dict().items():
            setattr(usuario, atributo, valor)

        try:
            usuario = await RepoUsuarioEscrita.adicionar(
                session=session, usuario=usuario, tipo_operacao=TipoOperacao.ATUALIZACAO
            )
        except Exception as erro:
            raise HTTPException(
                detail=f"Erro ao atualizar usuario: {erro}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return usuario

    @staticmethod
    async def deletar_por_id(session: AsyncSession, id: Uuid) -> str:
        usuario = await RepoUsuarioLeitura.consultar_por_id(session=session, id=id)

        if not usuario:
            raise UsuarioNaoEncontrado

        try:
            await RepoUsuarioEscrita.remover(session=session, usuario=usuario)
        except Exception as erro:
            raise HTTPException(
                detail=f"Erro ao deletar usuário: {erro}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return "Usuário deletado!"
