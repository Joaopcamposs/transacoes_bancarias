# noinspection PyUnresolvedReferences
def start_mappers() -> None:
    """Inicializa os mapeamentos ORM imperativo. Apenas importando, todos os mapeamentos são realizados."""
    from infra.database import mapper_registry as mapper_registry

    if mapper_registry.mappers:
        return

    from business_contexts.repository.orm.imperative.user import (
        user_mapper as user_mapper,
    )
    from business_contexts.repository.orm.imperative.client import (
        client_mapper as client_mapper,
    )
    from business_contexts.repository.orm.imperative.bank_account import (
        account_mapper as account_mapper,
    )
    from business_contexts.repository.orm.imperative.bank_transaction import (
        bank_transaction_mapper as bank_transaction_mapper,
    )
