from datetime import timedelta, datetime, UTC

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Annotated

from business_contexts.domain.aggregates.user import User
from business_contexts.domain.entities.user import UserEntity
from business_contexts.domain.exceptions import (
    MissingPermission,
    CouldNotValidateCredentials,
    ExpiredLogin,
)
from business_contexts.repository.domain_repo.user import UserDomainRepo
from business_contexts.utils.constants import SECRET_KEY, ALGORITHM, oauth2_scheme
from business_contexts.domain.entities.security import TokenData
from business_contexts.repository.query_repo.user import UserQueryRepo
from libs.ddd.adapters.viewers import Filters


async def authenticate_user(email: str, password: str) -> User | None:
    """Autentica um usuário verificando email e senha."""
    user = await UserDomainRepo().query_by_email(email=email)

    if not user:
        return None
    if not user.verify_password(password=password):
        return None

    return user


def create_token(data: dict, expiration_time: int | None = None) -> str:
    """Cria um token JWT com os dados fornecidos e tempo de expiração."""
    token_data: dict = data.copy()

    if expiration_time:
        expiration: datetime = datetime.now(UTC) + timedelta(expiration_time)
    else:
        expiration = datetime.now(UTC) + timedelta(minutes=15)
    token_data.update({"exp": expiration})
    encoded_token: str = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserEntity:
    """Obtém o usuário atual a partir do token JWT."""
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CouldNotValidateCredentials
        token_data = TokenData(email=email)
    except ExpiredSignatureError as error:
        raise ExpiredLogin from error
    except InvalidTokenError as error:
        raise CouldNotValidateCredentials from error
    user = await UserQueryRepo().query_one_by_filters(
        Filters({"email": token_data.email})
    )
    if user is None:
        raise CouldNotValidateCredentials
    return user


async def get_current_admin_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserEntity:
    """Obtém o usuário atual e verifica se é administrador."""
    user: UserEntity = await get_current_user(
        token=token,
    )
    if not user.is_admin:
        raise MissingPermission
    return user
