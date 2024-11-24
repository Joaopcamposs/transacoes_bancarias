from uuid import UUID

from sqlalchemy import select, insert, delete, update, Uuid
from sqlalchemy.orm import joinedload

from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.repositorio.orm.declarativo.conta_bancaria import (
    ContaBancariaDB,
)
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class ContaBancariaRepoDominio(RepositorioDominio):
    async def consultar_por_id(self, id: Uuid) -> Conta | None:
        async with self:
            conta_bancaria = (
                (
                    await self.session.execute(
                        select(ContaBancariaDB)
                        .options(joinedload(ContaBancariaDB.transacoes))
                        .filter_by(id=id)
                    )
                )
                .unique()
                .scalar_one_or_none()
            )

            if not conta_bancaria:
                return None

            agregado = Conta(
                id=conta_bancaria.id,
                numero_da_conta=conta_bancaria.numero_da_conta,
                saldo=conta_bancaria.saldo,
                cpf_cliente=conta_bancaria.cpf_cliente,
                transacoes=[
                    Transacao(
                        id=transacao.id,
                        tipo=transacao.tipo,
                        valor=transacao.valor,
                        data=transacao.data,
                        numero_da_conta=transacao.numero_da_conta,
                        numero_da_conta_destino=transacao.numero_da_conta_destino,
                    )
                    for transacao in conta_bancaria.transacoes
                ],
            )
        return agregado

    async def consultar_por_numero_da_conta(self, numero_da_conta: str) -> Conta | None:
        async with self:
            conta_bancaria = (
                (
                    await self.session.execute(
                        select(ContaBancariaDB)
                        .options(joinedload(ContaBancariaDB.transacoes))
                        .filter_by(numero_da_conta=numero_da_conta)
                    )
                )
                .unique()
                .scalar_one_or_none()
            )

            if not conta_bancaria:
                return None

            agregado = Conta(
                id=conta_bancaria.id,
                numero_da_conta=conta_bancaria.numero_da_conta,
                saldo=conta_bancaria.saldo,
                cpf_cliente=conta_bancaria.cpf_cliente,
                transacoes=[
                    Transacao(
                        id=transacao.id,
                        tipo=transacao.tipo,
                        valor=transacao.valor,
                        data=transacao.data,
                        numero_da_conta=transacao.numero_da_conta,
                        numero_da_conta_destino=transacao.numero_da_conta_destino,
                    )
                    for transacao in conta_bancaria.transacoes
                ],
            )
        return agregado

    async def adicionar(
        self,
        conta: Conta,
        tipo_operacao: TipoOperacao,
    ) -> UUID:
        async with self:
            try:
                dados = {
                    "numero_da_conta": conta.numero_da_conta,
                    "saldo": conta.saldo,
                    "cpf_cliente": conta.cpf_cliente,
                }

                match tipo_operacao:
                    case TipoOperacao.INSERCAO:
                        operacao = (
                            insert(ContaBancariaDB)
                            .values(dados)
                            .returning(ContaBancariaDB.id)
                        )
                        resultado = await self.session.execute(operacao)

                    case TipoOperacao.ATUALIZACAO:
                        operacao = (
                            update(ContaBancariaDB)
                            .where(ContaBancariaDB.id == conta.id)
                            .values(dados)
                        )
                        await self.session.execute(operacao)

                await self.commit()
            except Exception as erro:
                await self.rollback()
                raise erro

            id_resultado: UUID | None = conta.id
            if not id_resultado:
                id_resultado = resultado.scalar_one_or_none()

        return id_resultado

    async def remover(self, conta: Conta) -> None:
        async with self:
            try:
                operacao = delete(ContaBancariaDB).where(ContaBancariaDB.id == conta.id)

                await self.session.execute(operacao)
                await self.commit()
            except Exception as erro:
                await self.rollback()
                raise erro
