from fastapi import Depends, APIRouter
from pydantic import UUID4

from business_contexts.services.executors.bank_transaction import (
    create_bank_transaction,
)
from business_contexts.domain.exceptions import BankTransactionNotFound
from business_contexts.repository.query_repo.bank_transaction import (
    BankTransactionQueryRepo,
)
from business_contexts.domain.entities.bank_transaction import (
    CreateBankTransaction,
    ReadBankTransaction,
)
from business_contexts.services.executors.security import get_current_user
from libs.ddd.adapters.viewers import Filters

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Transacao Bancaria"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/transacao_bancarias", response_model=list[ReadBankTransaction])
async def list_transactions(
    id: UUID4 | None = None,
) -> list:
    """Lista transações bancárias com filtro opcional por ID."""
    filters = Filters(
        {
            "id": id,
        }
    )

    transactions = await BankTransactionQueryRepo().query_by_filters(filters=filters)

    if not transactions:
        raise BankTransactionNotFound

    return transactions


@router.post("/transacao_bancaria", response_model=ReadBankTransaction)
async def register(
    new_bank_transaction: CreateBankTransaction,
) -> ReadBankTransaction:
    """Cadastra uma nova transação bancária (depósito, saque ou transferência)."""
    bank_transaction = await create_bank_transaction(
        bank_transaction=new_bank_transaction
    )
    return bank_transaction
