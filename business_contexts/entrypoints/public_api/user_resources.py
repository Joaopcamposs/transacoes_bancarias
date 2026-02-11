from fastapi import Depends, APIRouter
from pydantic import UUID4

from business_contexts.domain.exceptions import UserNotFound
from business_contexts.repository.query_repo.user import UserQueryRepo
from business_contexts.domain.entities.user import (
    CreateUser,
    ReadUser,
    UpdateUser,
)
from business_contexts.services.executors.security import get_current_admin_user
from business_contexts.services.executors.user import (
    delete_user,
    create_user,
    update_user,
)
from libs.ddd.adapters.viewers import Filters

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Usuarios"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/usuarios", response_model=list[ReadUser])
async def list_users(
    id: UUID4 | None = None,
    email: str | None = None,
) -> list:
    """Lista usuários com filtros opcionais por ID e email."""
    filters = Filters(
        {
            "id": id,
            "email": email,
        }
    )

    users = await UserQueryRepo().query_by_filters(filters=filters)

    if not users:
        raise UserNotFound

    return users


@router.post("/usuario", response_model=ReadUser)
async def register(
    new_user: CreateUser,
) -> ReadUser:
    """Cadastra um novo usuário."""
    user = await create_user(user=new_user)
    return user


@router.put("/usuario", response_model=ReadUser)
async def update(
    updated_user: UpdateUser,
    id: UUID4 | None = None,
    email: str | None = None,
) -> ReadUser:
    """Atualiza os dados de um usuário existente."""
    filters = Filters(
        {
            "id": id,
            "email": email,
        }
    )

    user = await UserQueryRepo().query_one_by_filters(filters=filters)

    if not user:
        raise UserNotFound

    updated_user._id = user.id
    user = await update_user(updated_user=updated_user)
    return user


@router.delete("/usuario")
async def remove(
    id: UUID4 | None = None,
    email: str | None = None,
) -> str:
    """Remove um usuário pelo ID ou email."""
    filters = Filters(
        {
            "id": id,
            "email": email,
        }
    )

    user = await UserQueryRepo().query_one_by_filters(filters=filters)

    if not user:
        raise UserNotFound

    deleted_user = await delete_user(id=user.id)
    return deleted_user
