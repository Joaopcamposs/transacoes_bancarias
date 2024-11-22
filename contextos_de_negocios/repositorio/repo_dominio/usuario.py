from uuid import UUID

from sqlalchemy import Uuid, select, insert, update, delete

from contextos_de_negocios.repositorio.orm.usuario import Usuario
from contextos_de_negocios.dominio.agregados.usuario import Usuario as UsuarioAgregado
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
from libs.ddd.adaptadores.repositorio import RepositorioDominio


class UsuarioRepoDominio(RepositorioDominio):
    async def consultar_por_id(self, id: Uuid) -> UsuarioAgregado | None:
        async with self:
            usuario = (
                await self.session.execute(select(Usuario).where(Usuario.id == id))
            ).scalar_one_or_none()

            if not usuario:
                return None

            agregado = UsuarioAgregado(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                adm=usuario.adm,
                ativo=usuario.ativo,
                senha=usuario.senha,
            )
        return agregado

    async def consultar_por_email(self, email: str) -> UsuarioAgregado | None:
        async with self:
            usuario = (
                await self.session.execute(
                    select(Usuario).where(Usuario.email == email)
                )
            ).scalar_one_or_none()

            if not usuario:
                return None

            agregado = UsuarioAgregado(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                adm=usuario.adm,
                ativo=usuario.ativo,
                senha=usuario.senha,
            )
        return agregado

    async def adicionar(
        self,
        usuario: UsuarioAgregado,
        tipo_operacao: TipoOperacao,
    ) -> UUID:
        async with self:
            try:
                dados = {
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "senha": usuario.senha,
                    "adm": usuario.adm,
                    "ativo": usuario.ativo,
                }

                match tipo_operacao:
                    case TipoOperacao.INSERCAO:
                        operacao = insert(Usuario).values(dados).returning(Usuario.id)

                        resultado = await self.session.execute(operacao)
                        await self.session.commit()

                    case TipoOperacao.ATUALIZACAO:
                        operacao = (
                            update(Usuario)
                            .where(Usuario.id == usuario.id)
                            .values(dados)
                        )

                        await self.session.execute(operacao)
                        await self.session.commit()
            except Exception as erro:
                await self.session.rollback()
                raise erro

            id_resultado: UUID | None = usuario.id
            if not id_resultado:
                id_resultado = resultado.scalar_one_or_none()

        return id_resultado

    async def remover(self, usuario: UsuarioAgregado) -> None:
        async with self:
            try:
                operacao = delete(Usuario).where(Usuario.id == usuario.id)

                await self.session.execute(operacao)
                await self.session.commit()
            except Exception as erro:
                await self.session.rollback()
                raise erro
