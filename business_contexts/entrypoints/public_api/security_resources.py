from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from business_contexts.services.executors.security import (
    get_current_user,
    authenticate_user,
    create_token,
)
from business_contexts.domain.exceptions import (
    ErrorGeneratingToken,
    IncorrectCredentials,
)
from business_contexts.domain.entities.security import Token
from business_contexts.domain.entities.user import ReadUser, UserEntity
from business_contexts.utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router: APIRouter = APIRouter(prefix="/api", tags=["Login"])


@router.get("/usuario/me", response_model=ReadUser)
async def read_current_user(
    current_user: UserEntity = Depends(get_current_user),
) -> UserEntity:
    """Retorna os dados do usuário autenticado atual."""
    return current_user


@router.post("/token", response_model=Token)
async def token_and_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Autentica o usuário e retorna um token JWT de acesso."""
    try:
        user = await authenticate_user(
            email=form_data.username, password=form_data.password
        )
        if not user:
            raise IncorrectCredentials
        access_token: str = create_token(
            data={"sub": user.email},
            expiration_time=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception as error:
        raise ErrorGeneratingToken(
            detail=f"Erro ao gerar token: {error}",
        )
