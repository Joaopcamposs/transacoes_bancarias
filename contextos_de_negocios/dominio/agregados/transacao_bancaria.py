from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from contextos_de_negocios.utils.tipos_basicos import NumeroDaConta


@dataclass
class Transacao:
    tipo: TipoTransacao
    valor: Decimal
    data: datetime
    numero_da_conta: NumeroDaConta
    numero_da_conta_destino: NumeroDaConta | None = None
    id: UUID | None = None

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        tipo: TipoTransacao,
        valor: Decimal,
        data: datetime,
        numero_da_conta: NumeroDaConta,
        numero_da_conta_destino: NumeroDaConta | None = None,
    ) -> "Transacao":
        return Transacao(
            tipo=tipo,
            valor=valor,
            data=data,
            numero_da_conta=numero_da_conta,
            numero_da_conta_destino=numero_da_conta_destino,
        )

    def cadastrar(self) -> None: ...

    def atualizar(self) -> None: ...

    def remover(self) -> None: ...
