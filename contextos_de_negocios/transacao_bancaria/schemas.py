from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID4

from contextos_de_negocios.transacao_bancaria.objetos_de_valor import TipoTransacao


class CadastrarTransacaoBancaria(BaseModel):
    tipo: TipoTransacao
    valor: Decimal
    numero_da_conta: str
    numero_da_conta_destino: str | None = None


class LerTransacaoBancaria(BaseModel):
    id: UUID4
    tipo: TipoTransacao
    valor: Decimal
    data: datetime
    numero_da_conta: str
    numero_da_conta_destino: str | None = None
