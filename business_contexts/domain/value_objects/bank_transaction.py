import enum


class TransactionType(enum.Enum):
    """Tipos de transações bancárias disponíveis no sistema."""

    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
