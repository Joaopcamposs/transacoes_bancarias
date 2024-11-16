from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.agregados.usuario import Usuario as UsuarioAgregado
from contextos_de_negocios.dominio.exceptions import (
    UsuarioNaoEncontrado,
    UsuarioJaCadastrado,
)
from contextos_de_negocios.repositorio.repo_consulta.usuario import (
    UsuarioRepoConsulta,
)
from contextos_de_negocios.repositorio.repo_dominio.usuario import UsuarioRepoDominio
from contextos_de_negocios.dominio.entidades.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
)
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
from libs.ddd.adaptadores.visualizadores import Filtros


async def cadastrar_usuario(
    session: AsyncSession,
    usuario: CadastrarUsuario,
    criptografar_senha: bool = True,
) -> UsuarioAgregado:
    usuario_com_mesmo_email = await UsuarioRepoConsulta(
        session=session
    ).consultar_um_por_filtros(Filtros({"email": usuario.email}))

    if usuario_com_mesmo_email:
        raise UsuarioJaCadastrado

    novo_usuario = UsuarioAgregado.retornar_agregado_para_cadastro(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        adm=usuario.adm,
        ativo=usuario.ativo,
        criptografar_senha=criptografar_senha,
    )

    id_resultado = await UsuarioRepoDominio(session=session).adicionar(
        usuario=novo_usuario,
        tipo_operacao=TipoOperacao.INSERCAO,
    )
    novo_usuario.id = id_resultado

    return novo_usuario


async def atualizar_usuario(
    session: AsyncSession, usuario_att: AtualizarUsuario
) -> UsuarioAgregado:
    usuario = await UsuarioRepoDominio(session=session).consultar_por_id(
        id=usuario_att._id
    )

    if not usuario:
        raise UsuarioNaoEncontrado

    usuario.atualizar(
        nome=usuario_att.nome,
        email=usuario_att.email,
        senha=usuario_att.senha,
        adm=usuario_att.adm,
        ativo=usuario_att.ativo,
    )

    await UsuarioRepoDominio(session=session).adicionar(
        usuario=usuario, tipo_operacao=TipoOperacao.ATUALIZACAO
    )

    return usuario


async def remover_usuario(session: AsyncSession, id: Uuid) -> str:
    usuario = await UsuarioRepoDominio(session=session).consultar_por_id(id=id)

    if not usuario:
        raise UsuarioNaoEncontrado

    await UsuarioRepoDominio(session=session).remover(usuario=usuario)

    return "Usuário deletado!"
