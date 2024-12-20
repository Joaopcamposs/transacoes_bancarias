from uuid import UUID

from sqlalchemy import insert, update, delete, Uuid, select

from contextos_de_negocios.dominio.agregados.cliente import (
    Cliente,
)
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class ClienteRepoDominio(RepositorioDominio):
    async def consultar_por_id(self, id: Uuid) -> Cliente | None:
        async with self:
            cliente = (
                await self.session.execute(select(Cliente).where(Cliente.id == id))
            ).scalar_one_or_none()

            if not cliente:
                return None

            agregado = Cliente(
                id=cliente.id,
                nome=cliente.nome,
                cpf=cliente.cpf,
            )
        return agregado

    async def adicionar(
        self,
        cliente: Cliente,
        tipo_operacao: TipoOperacao,
    ) -> UUID:
        async with self:
            try:
                dados = {
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                }

                match tipo_operacao:
                    case TipoOperacao.INSERCAO:
                        operacao = insert(Cliente).values(dados).returning(Cliente.id)
                        resultado = await self.session.execute(operacao)

                    case TipoOperacao.ATUALIZACAO:
                        operacao = (
                            update(Cliente)
                            .where(Cliente.id == cliente.id)
                            .values(dados)
                        )
                        await self.session.execute(operacao)

                await self.commit()
            except Exception as erro:
                await self.rollback()
                raise erro

            id_resultado: UUID | None = cliente.id
            if not id_resultado:
                id_resultado = resultado.scalar_one_or_none()

        return id_resultado

    async def remover(self, cliente: Cliente) -> None:
        async with self:
            try:
                operacao = delete(Cliente).where(Cliente.id == cliente.id)

                await self.session.execute(operacao)
                await self.commit()
            except Exception as erro:
                await self.rollback()
                raise erro
