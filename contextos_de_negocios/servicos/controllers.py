from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from contextos_de_negocios.servicos.exceptions import NaoFoiPossivelValidarAsCredenciais
from contextos_de_negocios.usuario.exceptions import PermissaoFaltando
from contextos_de_negocios.usuario.models import Usuario
from contextos_de_negocios.utils.constantes import SECRET_KEY, ALGORITHM
from infra.database import get_db
from contextos_de_negocios.servicos.schemas import TokenData
from contextos_de_negocios.usuario.repositorio import RepoUsuarioLeitura

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Servicos:
    @staticmethod
    def verificar_senha(senha: str, senha_criptografada: str) -> bool:
        senhas_conferem = pwd_context.verify(secret=senha, hash=senha_criptografada)
        return senhas_conferem

    @staticmethod
    def criptografar_senha(senha: str) -> str:
        senha_criptografada = pwd_context.hash(secret=senha)
        return senha_criptografada

    @staticmethod
    async def autenticar_usuario(
        session: AsyncSession, email: str, senha: str
    ) -> Usuario | None:
        usuario = await RepoUsuarioLeitura.consultar_por_email(
            session=session, email=email
        )

        if not usuario:
            return None
        if not Servicos.verificar_senha(senha=senha, senha_criptografada=usuario.senha):
            return None

        return usuario

    @staticmethod
    def criar_token(data: dict, tempo_de_expiracao: int | None = None) -> str:
        dados_token = data.copy()

        if tempo_de_expiracao:
            expiracao = datetime.utcnow() + timedelta(tempo_de_expiracao)
        else:
            expiracao = datetime.utcnow() + timedelta(minutes=15)
        dados_token.update({"exp": expiracao})
        token_codificado = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)

        return token_codificado

    @staticmethod
    async def obter_usuario_atual(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_db),
    ):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise NaoFoiPossivelValidarAsCredenciais(
                    headers={"WWW-Authenticate": "Bearer"}
                )
            dados_token = TokenData(email=email)
        except InvalidTokenError:
            raise NaoFoiPossivelValidarAsCredenciais(
                headers={"WWW-Authenticate": "Bearer"}
            )
        usuario = await RepoUsuarioLeitura.consultar_por_email(
            session=session, email=dados_token.email
        )
        if usuario is None:
            raise NaoFoiPossivelValidarAsCredenciais(
                headers={"WWW-Authenticate": "Bearer"}
            )
        return usuario

    @staticmethod
    async def obter_usuario_atual_adm(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_db),
    ):
        usuario = await Servicos.obter_usuario_atual(
            token=token,
            session=session,
        )
        if not usuario.adm:
            raise PermissaoFaltando
        return usuario


UsuarioAtual = Annotated[Usuario, Depends(Servicos.obter_usuario_atual)]
UsuarioAtualADM = Annotated[Usuario, Depends(Servicos.obter_usuario_atual_adm)]
