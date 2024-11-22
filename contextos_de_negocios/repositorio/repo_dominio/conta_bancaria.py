from uuid import UUID

from sqlalchemy import select, insert, delete, update, Uuid
from sqlalchemy.orm import joinedload

from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class ContaBancariaRepoDominio(RepositorioDominio):
    async def consultar_por_id(self, id: Uuid) -> Conta | None:
        async with self:
            conta_bancaria = (
                (
                    await self.session.execute(
                        select(Conta)
                        .options(joinedload(Conta.transacoes))
                        .filter_by(id=id)
                        .with_for_update()
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
                transacoes=conta_bancaria.transacoes,
            )
        return agregado

    async def consultar_por_numero_da_conta(self, numero_da_conta: str) -> Conta | None:
        async with self:
            conta_bancaria = (
                (
                    await self.session.execute(
                        select(Conta)
                        .options(joinedload(Conta.transacoes))
                        .filter_by(numero_da_conta=numero_da_conta)
                        .with_for_update()
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
                transacoes=conta_bancaria.transacoes,
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
                        operacao = insert(Conta).values(dados).returning(Conta.id)

                        resultado = await self.session.execute(operacao)
                        await self.session.commit()

                    case TipoOperacao.ATUALIZACAO:
                        operacao = (
                            update(Conta).where(Conta.id == conta.id).values(dados)
                        )

                        await self.session.execute(operacao)
                        await self.session.commit()
            except Exception as erro:
                await self.session.rollback()
                raise erro

            id_resultado: UUID | None = conta.id
            if not id_resultado:
                id_resultado = resultado.scalar_one_or_none()

        return id_resultado

    async def remover(self, conta: Conta) -> None:
        async with self:
            try:
                operacao = delete(Conta).where(Conta.id == conta.id)

                await self.session.execute(operacao)
                await self.session.commit()
            except Exception as erro:
                await self.session.rollback()
                raise erro
