from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.exceptions import (
    ClienteNaoEncontrado,
    ContaBancariaNaoEncontrado,
    ContaBancariaJaCadastrado,
    ErroAoAtualizarContaBancaria,
    ErroAoDeletarContaBancaria,
)
from contextos_de_negocios.repositorio.repo_consulta.cliente import ClienteRepoConsulta
from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from contextos_de_negocios.repositorio.repo_consulta.conta_bancaria import (
    ContaBancariaRepoConsulta,
)
from contextos_de_negocios.repositorio.repo_dominio.conta_bancaria import (
    ContaBancariaRepoDominio,
)
from contextos_de_negocios.dominio.entidades.conta_bancaria import (
    CadastrarContaBancaria,
    AtualizarContaBancaria,
)
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
from libs.ddd.adaptadores.visualizadores import Filtros


class ContaBancariaControllers:
    @staticmethod
    async def cadastrar(
        session: AsyncSession,
        conta_bancaria: CadastrarContaBancaria,
    ) -> ContaBancaria:
        conta_bancaria_no_banco = (
            await ContaBancariaRepoConsulta.consultar_por_numero_da_conta(
                session=session, numero_da_conta=conta_bancaria.numero_da_conta
            )
        )
        if conta_bancaria_no_banco:
            raise ContaBancariaJaCadastrado

        # Verifica se o CPF existe
        cliente = await ClienteRepoConsulta(session=session).consultar_um_por_filtros(
            Filtros({"cpf": conta_bancaria.cpf_cliente})
        )
        if not cliente:
            raise ClienteNaoEncontrado

        novo_conta_bancaria = Conta(
            numero_da_conta=conta_bancaria.numero_da_conta,
            saldo=conta_bancaria.saldo,
            cpf_cliente=conta_bancaria.cpf_cliente,
        ).nova_conta()

        novo_conta_bancaria = await ContaBancariaRepoDominio.adicionar(
            session=session,
            conta_bancaria=novo_conta_bancaria,
            tipo_operacao=TipoOperacao.INSERCAO,
        )

        return novo_conta_bancaria

    @staticmethod
    async def atualizar_por_id(
        session: AsyncSession,
        id: Uuid,
        conta_bancaria_att: AtualizarContaBancaria,
    ) -> ContaBancaria:
        conta_bancaria = await ContaBancariaRepoConsulta.consultar_por_id(
            session=session, id=id
        )

        if not conta_bancaria:
            raise ContaBancariaNaoEncontrado

        for atributo, valor in conta_bancaria_att.dict().items():
            setattr(conta_bancaria, atributo, valor)

        try:
            conta_bancaria = await ContaBancariaRepoDominio.adicionar(
                session=session,
                conta_bancaria=conta_bancaria,
                tipo_operacao=TipoOperacao.ATUALIZACAO,
            )
        except Exception as erro:
            raise ErroAoAtualizarContaBancaria(
                detail=f"Erro ao atualizar conta_bancaria: {erro}",
            )
        return conta_bancaria

    @staticmethod
    async def deletar_por_id(session: AsyncSession, id: Uuid) -> str:
        conta_bancaria = await ContaBancariaRepoConsulta.consultar_por_id(
            session=session, id=id
        )

        if not conta_bancaria:
            raise ContaBancariaNaoEncontrado

        try:
            await ContaBancariaRepoDominio.remover(
                session=session, conta_bancaria=conta_bancaria
            )
        except Exception as erro:
            raise ErroAoDeletarContaBancaria(
                detail=f"Erro ao deletar conta bancaria: {erro}",
            )

        return "ContaBancaria deletado!"
