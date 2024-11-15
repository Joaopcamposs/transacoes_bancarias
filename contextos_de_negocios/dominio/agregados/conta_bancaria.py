from dataclasses import dataclass
from uuid import UUID, uuid4

from _decimal import Decimal

from contextos_de_negocios.dominio.exceptions import (
    SaldoInsuficienteParaRealizarTransacao,
)
from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from contextos_de_negocios.repositorio.orm.transacao_bancaria import TransacaoBancaria
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
)
from contextos_de_negocios.utils.tipos_basicos import NumeroDaConta, CPF


@dataclass
class Conta:
    numero_da_conta: NumeroDaConta | str
    saldo: Decimal
    cpf_cliente: CPF | str
    id: UUID = uuid4()

    @staticmethod
    def _validar_valor_da_operacao(valor: Decimal) -> None:
        if valor < 0:
            raise ValueError("Valor da operação não pode ser negativo")

    def _validar_saldo(self, valor: Decimal) -> None:
        if self.saldo < valor:
            raise SaldoInsuficienteParaRealizarTransacao

    def nova_transacao(
        self, transacao_bancaria: CadastrarTransacaoBancaria
    ) -> TransacaoBancaria:
        self._validar_valor_da_operacao(transacao_bancaria.valor)

        match transacao_bancaria.tipo:
            case TipoTransacao.SAQUE:
                return self.realizar_saque(transacao_bancaria.valor)
            case TipoTransacao.DEPOSITO:
                return self.realizar_deposito(transacao_bancaria.valor)
            case TipoTransacao.TRANSFERENCIA:
                return self.realizar_transferencia(
                    transacao_bancaria.valor, transacao_bancaria.numero_da_conta_destino
                )
            case _:
                raise ValueError("Tipo de transação inválido")

    def realizar_saque(self, valor: Decimal) -> TransacaoBancaria:
        self._validar_saldo(valor)

        self.saldo -= valor
        return TransacaoBancaria(
            tipo=TipoTransacao.SAQUE.value,
            valor=valor,
            numero_da_conta=self.numero_da_conta,
        )

    def realizar_deposito(self, valor: Decimal) -> TransacaoBancaria:
        self.saldo += valor
        return TransacaoBancaria(
            tipo=TipoTransacao.DEPOSITO.value,
            valor=valor,
            numero_da_conta=self.numero_da_conta,
        )

    def realizar_transferencia(
        self, valor: Decimal, numero_da_conta_destino: str
    ) -> TransacaoBancaria:
        self._validar_saldo(valor)

        self.saldo -= valor
        return TransacaoBancaria(
            tipo=TipoTransacao.TRANSFERENCIA.value,
            valor=valor,
            numero_da_conta=self.numero_da_conta,
            numero_da_conta_destino=numero_da_conta_destino,
        )

    def nova_conta(self) -> ContaBancaria:
        return ContaBancaria(
            numero_da_conta=NumeroDaConta(self.numero_da_conta),
            saldo=Decimal(self.saldo),
            cpf_cliente=CPF.somente_digitos(str(self.cpf_cliente)),
        )

    def atualizar_conta(self) -> ContaBancaria:
        return ContaBancaria(
            id=self.id,
            numero_da_conta=self.numero_da_conta,
            cpf_cliente=self.cpf_cliente,
            saldo=self.saldo,
        )
