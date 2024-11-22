from dataclasses import dataclass, field
from uuid import UUID

from _decimal import Decimal

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.exceptions import (
    SaldoInsuficienteParaRealizarTransacao,
)
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
)
from contextos_de_negocios.dominio.regras_de_negocio.transacao_bancaria import (
    obter_hora_local,
)
from contextos_de_negocios.utils.tipos_basicos import NumeroDaConta, CPF


@dataclass
class Conta:
    numero_da_conta: NumeroDaConta | str
    saldo: Decimal
    cpf_cliente: CPF | str
    id: UUID | None = None
    transacoes: list[Transacao] = field(default_factory=list)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls, numero_da_conta: NumeroDaConta, saldo: Decimal, cpf_cliente: CPF
    ) -> "Conta":
        return Conta(
            numero_da_conta=numero_da_conta, saldo=saldo, cpf_cliente=cpf_cliente
        )

    @staticmethod
    def _validar_valor_da_operacao(valor: Decimal) -> None:
        if valor < 0:
            raise ValueError("Valor da operação não pode ser negativo")

    def _validar_saldo(self, valor: Decimal) -> None:
        if self.saldo < valor:
            raise SaldoInsuficienteParaRealizarTransacao

    def nova_transacao(
        self, transacao_bancaria: CadastrarTransacaoBancaria
    ) -> Transacao:
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

    def realizar_saque(self, valor: Decimal) -> Transacao:
        self._validar_saldo(valor)

        self.saldo -= valor
        return Transacao.retornar_agregado_para_cadastro(
            tipo=TipoTransacao.SAQUE,
            valor=valor,
            numero_da_conta=self.numero_da_conta,
            data=obter_hora_local(),
        )

    def realizar_deposito(self, valor: Decimal) -> Transacao:
        self.saldo += valor
        return Transacao.retornar_agregado_para_cadastro(
            tipo=TipoTransacao.DEPOSITO,
            valor=valor,
            numero_da_conta=self.numero_da_conta,
            data=obter_hora_local(),
        )

    def realizar_transferencia(
        self, valor: Decimal, numero_da_conta_destino: str
    ) -> Transacao:
        self._validar_saldo(valor)

        self.saldo -= valor
        return Transacao.retornar_agregado_para_cadastro(
            tipo=TipoTransacao.TRANSFERENCIA,
            valor=valor,
            numero_da_conta=self.numero_da_conta,
            numero_da_conta_destino=numero_da_conta_destino,
            data=obter_hora_local(),
        )

    def cadastrar(self) -> None: ...

    def atualizar(self, numero_da_conta: NumeroDaConta, cpf_cliente: CPF) -> None:
        self.numero_da_conta = numero_da_conta
        self.cpf_cliente = cpf_cliente

    def remover(self) -> None: ...
