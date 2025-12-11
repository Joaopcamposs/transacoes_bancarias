from uuid import UUID

from sqlalchemy import insert

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class TransacaoBancariaRepoDominio(RepositorioDominio):
    async def adicionar(
        self,
        transacao: Transacao,
    ) -> UUID:
        async with self:
            try:
                dados = {
                    "tipo": transacao.tipo.value,
                    "valor": transacao.valor,
                    "data": transacao.data,
                    "numero_da_conta": transacao.numero_da_conta,
                    "numero_da_conta_destino": transacao.numero_da_conta_destino,
                }
                operacao = insert(Transacao).values(dados).returning(Transacao.id)
                resultado = await self.session.execute(operacao)

                await self.commit()
            except Exception as erro:
                await self.rollback()
                raise erro

            id_resultado: UUID | None = transacao.id
            if not id_resultado:
                id_resultado = resultado.scalar_one_or_none()

        return id_resultado
