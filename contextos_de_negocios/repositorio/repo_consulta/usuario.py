from typing import Sequence

from sqlalchemy import select

from contextos_de_negocios.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocios.repositorio.orm.usuario import Usuario
from libs.ddd.adaptadores.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores import Filtros


class UsuarioRepoConsulta(RepositorioConsulta):
    async def consultar_por_filtros(
        self, filtros: Filtros
    ) -> Sequence[UsuarioEntidade]:
        async with self:
            usuarios = (
                (await self.session.execute(select(Usuario).filter_by(**filtros)))
                .scalars()
                .all()
            )

            usuarios_entidade = [
                UsuarioEntidade(
                    id=usuario.id,
                    nome=usuario.nome,
                    email=usuario.email,
                    adm=usuario.adm,
                    ativo=usuario.ativo,
                    _senha=usuario.senha,
                )
                for usuario in usuarios
            ]

        return usuarios_entidade

    async def consultar_um_por_filtros(
        self, filtros: Filtros
    ) -> UsuarioEntidade | None:
        async with self:
            usuario = (
                await self.session.execute(select(Usuario).filter_by(**filtros))
            ).scalar_one_or_none()
            if not usuario:
                return None

            usuario_entidade = UsuarioEntidade(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                adm=usuario.adm,
                ativo=usuario.ativo,
                _senha=usuario.senha,
            )

        return usuario_entidade
