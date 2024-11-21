from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from contextos_de_negocios.servicos.executores.seguranca import (
    obter_usuario_atual,
    autenticar_usuario,
    criar_token,
)
from contextos_de_negocios.dominio.exceptions import (
    ErroAoGerarToken,
    CredenciaisIncorretas,
)
from contextos_de_negocios.dominio.entidades.seguranca import Token
from contextos_de_negocios.repositorio.orm.usuario import Usuario
from contextos_de_negocios.dominio.entidades.usuario import LerUsuario
from contextos_de_negocios.utils.constantes import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api", tags=["Login"])


@router.get("/usuario/me", response_model=LerUsuario)
async def ler_usuario_atual(
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return usuario_atual


@router.post("/token", response_model=Token)
async def token_e_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        usuario = await autenticar_usuario(
            email=form_data.username, senha=form_data.password
        )
        if not usuario:
            raise CredenciaisIncorretas
        access_token = criar_token(
            data={"sub": usuario.email},
            tempo_de_expiracao=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception as erro:
        raise ErroAoGerarToken(
            detail=f"Erro ao gerar token: {erro}",
        )
