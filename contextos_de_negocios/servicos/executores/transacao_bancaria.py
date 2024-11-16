from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.exceptions import ContaBancariaNaoEncontrado
from contextos_de_negocios.repositorio.repo_consulta.conta_bancaria import (
    ContaBancariaRepoConsulta,
)
from contextos_de_negocios.repositorio.repo_dominio.conta_bancaria import (
    ContaBancariaRepoDominio,
)
from contextos_de_negocios.repositorio.repo_dominio.transacao_bancaria import (
    TransacaoBancariaRepoDominio,
)
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
)
from libs.ddd.adaptadores.visualizadores import Filtros


async def cadastrar_transacao_bancaria(
    session: AsyncSession,
    transacao_bancaria: CadastrarTransacaoBancaria,
) -> Transacao:
    conta_origem = await ContaBancariaRepoDominio(
        session=session
    ).consultar_por_numero_da_conta(numero_da_conta=transacao_bancaria.numero_da_conta)
    if not conta_origem:
        raise ContaBancariaNaoEncontrado

    if transacao_bancaria.numero_da_conta_destino:
        conta_destino = await ContaBancariaRepoConsulta(
            session=session
        ).consultar_um_por_filtros(
            Filtros({"numero_da_conta": transacao_bancaria.numero_da_conta_destino})
        )
        if not conta_destino:
            raise ContaBancariaNaoEncontrado

    novo_transacao_bancaria = conta_origem.nova_transacao(transacao_bancaria)
    id_resultado = await TransacaoBancariaRepoDominio(session=session).adicionar(
        transacao=novo_transacao_bancaria,
    )
    novo_transacao_bancaria.id = id_resultado

    return novo_transacao_bancaria
