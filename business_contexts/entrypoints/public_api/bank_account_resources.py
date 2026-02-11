from fastapi import Depends, APIRouter
from pydantic import UUID4

from business_contexts.domain.exceptions import BankAccountNotFound
from business_contexts.repository.query_repo.bank_account import (
    BankAccountQueryRepo,
)
from business_contexts.domain.entities.bank_account import (
    CreateBankAccount,
    UpdateBankAccount,
    ReadBankAccount,
)
from business_contexts.services.executors.bank_account import (
    create_account,
    update_account,
    delete_account,
)
from business_contexts.services.executors.security import get_current_user
from libs.ddd.adapters.viewers import Filters

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Conta Bancaria"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/conta_bancarias",
    response_model=list[ReadBankAccount],
)
async def list_accounts(
    id: UUID4 | None = None,
    account_number: str | None = None,
    list_transactions: bool = False,
) -> list:
    """Lista contas bancárias com filtros opcionais por ID, número da conta e transações."""
    filters = Filters(
        {
            "id": id,
            "account_number": account_number,
            "list_transactions": list_transactions,
        }
    )

    bank_accounts = await BankAccountQueryRepo().query_by_filters(filters=filters)

    if not bank_accounts:
        raise BankAccountNotFound

    return bank_accounts


@router.post("/conta_bancaria", response_model=ReadBankAccount)
async def register(
    new_bank_account: CreateBankAccount,
) -> ReadBankAccount:
    """Cadastra uma nova conta bancária."""
    bank_account = await create_account(bank_account=new_bank_account)
    return bank_account


@router.put("/conta_bancaria", response_model=ReadBankAccount)
async def update(
    updated_bank_account: UpdateBankAccount,
    id: UUID4 | None = None,
    account_number: str | None = None,
) -> ReadBankAccount:
    """Atualiza os dados de uma conta bancária existente."""
    filters = Filters(
        {
            "id": id,
            "account_number": account_number,
        }
    )

    bank_account = await BankAccountQueryRepo().query_one_by_filters(filters=filters)

    if not bank_account:
        raise BankAccountNotFound

    updated_bank_account._old_account_number = bank_account.account_number
    bank_account = await update_account(
        updated_bank_account=updated_bank_account,
    )
    return bank_account


@router.delete("/conta_bancaria")
async def remove(
    id: UUID4 | None = None,
    account_number: str | None = None,
) -> str:
    """Remove uma conta bancária pelo ID ou número da conta."""
    filters = Filters(
        {
            "id": id,
            "account_number": account_number,
        }
    )

    bank_account = await BankAccountQueryRepo().query_one_by_filters(filters=filters)

    if not bank_account:
        raise BankAccountNotFound

    deleted_bank_account = await delete_account(id=bank_account.id)
    return deleted_bank_account
