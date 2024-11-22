from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from typing_extensions import Annotated

from contextos_de_negocios.dominio.agregados.usuario import Usuario
from contextos_de_negocios.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocios.dominio.exceptions import (
    PermissaoFaltando,
    NaoFoiPossivelValidarAsCredenciais,
)
from contextos_de_negocios.repositorio.repo_dominio.usuario import UsuarioRepoDominio
from contextos_de_negocios.utils.constantes import SECRET_KEY, ALGORITHM, oauth2_scheme
from contextos_de_negocios.dominio.entidades.seguranca import TokenData
from contextos_de_negocios.repositorio.repo_consulta.usuario import UsuarioRepoConsulta
from libs.ddd.adaptadores.visualizadores import Filtros


async def autenticar_usuario(email: str, senha: str) -> Usuario | None:
    usuario = await UsuarioRepoDominio().consultar_por_email(email=email)

    if not usuario:
        return None
    if not usuario.verificar_senha(senha=senha):
        return None

    return usuario


def criar_token(data: dict, tempo_de_expiracao: int | None = None) -> str:
    dados_token = data.copy()

    if tempo_de_expiracao:
        expiracao = datetime.utcnow() + timedelta(tempo_de_expiracao)
    else:
        expiracao = datetime.utcnow() + timedelta(minutes=15)
    dados_token.update({"exp": expiracao})
    token_codificado = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)

    return token_codificado


async def obter_usuario_atual(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UsuarioEntidade:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise NaoFoiPossivelValidarAsCredenciais(
                headers={"WWW-Authenticate": "Bearer"}
            )
        dados_token = TokenData(email=email)
    except InvalidTokenError:
        raise NaoFoiPossivelValidarAsCredenciais(headers={"WWW-Authenticate": "Bearer"})
    usuario = await UsuarioRepoConsulta().consultar_um_por_filtros(
        Filtros({"email": dados_token.email})
    )
    if usuario is None:
        raise NaoFoiPossivelValidarAsCredenciais(headers={"WWW-Authenticate": "Bearer"})
    return usuario


async def obter_usuario_atual_adm(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    usuario = await obter_usuario_atual(
        token=token,
    )
    if not usuario.adm:
        raise PermissaoFaltando
    return usuario
