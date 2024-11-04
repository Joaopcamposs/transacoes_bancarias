from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.conta_bancaria.exceptions import ContaBancariaNaoEncontrado
from contextos_de_negocios.conta_bancaria.repositorio import (
    RepoContaBancariaLeitura,
    RepoContaBancariaDominio,
)
from contextos_de_negocios.transacao_bancaria.models import TransacaoBancaria
from contextos_de_negocios.transacao_bancaria.repositorio import (
    RepoTransacaoBancariaEscrita,
)
from contextos_de_negocios.transacao_bancaria.schemas import (
    CadastrarTransacaoBancaria,
)


async def cadastrar_transacao_bancaria(
    session: AsyncSession,
    transacao_bancaria: CadastrarTransacaoBancaria,
) -> TransacaoBancaria:
    conta_origem = await RepoContaBancariaDominio.consultar_por_numero_da_conta(
        session=session, numero_da_conta=transacao_bancaria.numero_da_conta
    )
    if not conta_origem:
        raise ContaBancariaNaoEncontrado

    if transacao_bancaria.numero_da_conta_destino:
        conta_destino = await RepoContaBancariaLeitura.consultar_por_numero_da_conta(
            session=session,
            numero_da_conta=transacao_bancaria.numero_da_conta_destino,
        )
        if not conta_destino:
            raise ContaBancariaNaoEncontrado

    novo_transacao_bancaria = conta_origem.nova_transacao(transacao_bancaria)
    novo_transacao_bancaria = await RepoTransacaoBancariaEscrita.adicionar(
        session=session,
        transacao_bancaria=novo_transacao_bancaria,
    )

    return novo_transacao_bancaria
