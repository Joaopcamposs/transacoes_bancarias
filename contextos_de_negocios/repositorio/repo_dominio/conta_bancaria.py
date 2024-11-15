from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.dominio.exceptions import ErroAoDeletarContaBancaria
from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao


class RepoContaBancariaDominio:
    @staticmethod
    async def consultar_por_numero_da_conta(
        session: AsyncSession, numero_da_conta: str
    ) -> Conta | None:
        conta_bancaria = (
            (
                await session.execute(
                    select(ContaBancaria).filter_by(numero_da_conta=numero_da_conta)
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
        )
        return agregado


class RepoContaBancariaEscrita:
    @staticmethod
    async def adicionar(
        session: AsyncSession,
        conta_bancaria: ContaBancaria,
        tipo_operacao: TipoOperacao,
    ) -> ContaBancaria:
        if tipo_operacao == TipoOperacao.INSERCAO:
            try:
                session.add(conta_bancaria)
                await session.commit()
                await session.refresh(conta_bancaria)
            except Exception as erro:
                await session.rollback()
                raise erro
        elif tipo_operacao == TipoOperacao.ATUALIZACAO:
            try:
                await session.merge(conta_bancaria)
                await session.commit()
                await session.refresh(conta_bancaria)
            except Exception as erro:
                await session.rollback()
                raise erro
        return conta_bancaria

    @staticmethod
    async def remover(session: AsyncSession, conta_bancaria: ContaBancaria) -> None:
        try:
            await session.delete(conta_bancaria)
            await session.commit()
        except Exception as erro:
            await session.rollback()
            raise ErroAoDeletarContaBancaria(
                detail=f"Erro ao deletar conta bancaria: {erro}",
            )
