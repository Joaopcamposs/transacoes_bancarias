from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from contextos_de_negocios.dominio.exceptions import (
    UsuarioNaoEncontrado,
    UsuarioJaCadastrado,
)
from contextos_de_negocios.repositorio.orm.usuario import Usuario
from contextos_de_negocios.repositorio.repo_consulta.usuario import (
    UsuarioRepoConsulta,
)
from contextos_de_negocios.repositorio.repo_dominio.usuario import UsuarioRepoDominio
from contextos_de_negocios.dominio.entidades.usuario import CadastrarEAtualizarUsuario
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class UsuarioControllers:
    @staticmethod
    async def cadastrar(
        session: AsyncSession,
        usuario: CadastrarEAtualizarUsuario,
        criptografar_senha: bool = True,
    ) -> Usuario:
        from contextos_de_negocios.servicos.executores.seguranca import Servicos

        usuario_no_banco = await UsuarioRepoConsulta.consultar_por_email(
            session=session, email=usuario.email
        )

        if usuario_no_banco:
            raise UsuarioJaCadastrado

        novo_usuario = Usuario(**usuario.dict())
        novo_usuario.email = novo_usuario.email.lower()
        if criptografar_senha:
            novo_usuario.senha = Servicos.criptografar_senha(novo_usuario.senha)

        try:
            novo_usuario = await UsuarioRepoDominio.adicionar(
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
        from contextos_de_negocios.servicos.executores.seguranca import Servicos

        usuario = await UsuarioRepoConsulta.consultar_por_id(session=session, id=id)

        if not usuario:
            raise UsuarioNaoEncontrado

        usuario_att.email = usuario_att.email.lower()
        usuario_att.senha = Servicos.criptografar_senha(usuario_att.senha)

        # Atualiza os dados do acessório
        for atributo, valor in usuario_att.dict().items():
            setattr(usuario, atributo, valor)

        try:
            usuario = await UsuarioRepoDominio.adicionar(
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
        usuario = await UsuarioRepoConsulta.consultar_por_id(session=session, id=id)

        if not usuario:
            raise UsuarioNaoEncontrado

        try:
            await UsuarioRepoDominio.remover(session=session, usuario=usuario)
        except Exception as erro:
            raise HTTPException(
                detail=f"Erro ao deletar usuário: {erro}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return "Usuário deletado!"
