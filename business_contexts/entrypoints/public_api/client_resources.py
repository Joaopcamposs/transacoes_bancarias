from fastapi import Depends, APIRouter
from pydantic import UUID4

from business_contexts.domain.exceptions import (
    ClientNotFound,
)
from business_contexts.repository.query_repo.client import ClientQueryRepo
from business_contexts.domain.entities.client import (
    CreateClient,
    ReadClient,
    UpdateClient,
)
from business_contexts.services.executors.client import (
    create_client,
    update_client,
    delete_client,
)
from business_contexts.services.executors.security import get_current_user
from libs.ddd.adapters.viewers import Filters

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Clientes"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/clientes", response_model=list[ReadClient])
async def list_clients(
    id: UUID4 | None = None,
    cpf: str | None = None,
) -> list:
    """Lista clientes com filtros opcionais por ID e CPF."""
    filters = Filters(
        {
            "id": id,
            "cpf": cpf,
        }
    )

    clients = await ClientQueryRepo().query_by_filters(filters=filters)

    if not clients:
        raise ClientNotFound

    return clients


@router.post("/cliente", response_model=ReadClient)
async def register(
    new_client: CreateClient,
) -> ReadClient:
    """Cadastra um novo cliente."""
    client = await create_client(client=new_client)
    return client


@router.put("/cliente", response_model=ReadClient)
async def update(
    updated_client: UpdateClient,
    id: UUID4 | None = None,
    cpf: str | None = None,
) -> ReadClient:
    """Atualiza os dados de um cliente existente."""
    filters = Filters(
        {
            "id": id,
            "cpf": cpf,
        }
    )

    client = await ClientQueryRepo().query_one_by_filters(filters=filters)

    if not client:
        raise ClientNotFound

    updated_client._id = client.id
    client = await update_client(updated_client=updated_client)
    return client


@router.delete("/cliente")
async def remove(
    id: UUID4 | None = None,
    cpf: str | None = None,
) -> str:
    """Remove um cliente pelo ID ou CPF."""
    filters = Filters(
        {
            "id": id,
            "cpf": cpf,
        }
    )

    client = await ClientQueryRepo().query_one_by_filters(filters=filters)

    if not client:
        raise ClientNotFound

    deleted_client = await delete_client(id=client.id)
    return deleted_client
