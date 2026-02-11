from sqlalchemy import Uuid

from business_contexts.domain.aggregates.user import User
from business_contexts.domain.exceptions import (
    UserNotFound,
    UserAlreadyRegistered,
)
from business_contexts.repository.query_repo.user import (
    UserQueryRepo,
)
from business_contexts.repository.domain_repo.user import UserDomainRepo
from business_contexts.domain.entities.user import (
    CreateUser,
    UpdateUser,
)
from business_contexts.utils.base_types import OperationType
from libs.ddd.adapters.viewers import Filters


async def create_user(
    user: CreateUser,
    encrypt_password: bool = True,
) -> User:
    """Cadastra um novo usuário, verificando se já existe um com o mesmo email."""
    user_with_same_email = await UserQueryRepo().query_one_by_filters(
        Filters({"email": user.email})
    )

    if user_with_same_email:
        raise UserAlreadyRegistered

    new_user = User.return_aggregate_for_creation(
        name=user.name,
        email=user.email,
        password=user.password,
        is_admin=user.is_admin,
        is_active=user.is_active,
        encrypt_password=encrypt_password,
    )

    result_id = await UserDomainRepo().add(
        user=new_user,
        operation_type=OperationType.INSERT,
    )
    new_user.id = result_id

    return new_user


async def update_user(updated_user: UpdateUser) -> User:
    """Atualiza os dados de um usuário existente."""
    user = await UserDomainRepo().query_by_id(id=updated_user._id)

    if not user:
        raise UserNotFound

    user.update(
        name=updated_user.name,
        email=updated_user.email,
        password=updated_user.password,
        is_admin=updated_user.is_admin,
        is_active=updated_user.is_active,
    )

    await UserDomainRepo().add(user=user, operation_type=OperationType.UPDATE)

    return user


async def delete_user(id: Uuid) -> str:
    """Remove um usuário pelo ID."""
    user = await UserDomainRepo().query_by_id(id=id)

    if not user:
        raise UserNotFound

    await UserDomainRepo().remove(user=user)

    return "Usuário deletado!"
