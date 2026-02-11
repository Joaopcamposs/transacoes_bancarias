from sqlalchemy import Uuid

from business_contexts.domain.aggregates.client import Client
from business_contexts.domain.exceptions import (
    ClientAlreadyRegistered,
    ClientNotFound,
)
from business_contexts.repository.query_repo.client import (
    ClientQueryRepo,
)
from business_contexts.repository.domain_repo.client import ClientDomainRepo
from business_contexts.domain.entities.client import (
    CreateClient,
    UpdateClient,
)
from business_contexts.utils.base_types import OperationType, CPF
from libs.ddd.adapters.viewers import Filters


async def create_client(
    client: CreateClient,
) -> Client:
    """Cadastra um novo cliente, verificando se já existe um com o mesmo CPF."""
    client_with_same_cpf = await ClientQueryRepo().query_one_by_filters(
        Filters({"cpf": client.cpf})
    )

    if client_with_same_cpf:
        raise ClientAlreadyRegistered

    new_client = Client.return_aggregate_for_creation(
        name=client.name,
        cpf=CPF(client.cpf),
    )
    result_id = await ClientDomainRepo().add(
        client=new_client,
        operation_type=OperationType.INSERT,
    )
    new_client.id = result_id

    return new_client


async def update_client(updated_client: UpdateClient) -> Client:
    """Atualiza os dados de um cliente existente."""
    client = await ClientDomainRepo().query_by_id(id=updated_client._id)

    if not client:
        raise ClientNotFound

    client.update(name=updated_client.name, cpf=CPF(updated_client.cpf))

    await ClientDomainRepo().add(client=client, operation_type=OperationType.UPDATE)
    return client


async def delete_client(id: Uuid) -> str:
    """Remove um cliente pelo ID."""
    client = await ClientDomainRepo().query_by_id(id=id)

    if not client:
        raise ClientNotFound

    await ClientDomainRepo().remove(client=client)

    return "Cliente deletado!"
