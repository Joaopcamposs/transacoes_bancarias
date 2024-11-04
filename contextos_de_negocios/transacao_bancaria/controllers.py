from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.conta_bancaria.exceptions import ContaBancariaNaoEncontrado
from contextos_de_negocios.conta_bancaria.repositorio import RepoContaBancariaLeitura
from contextos_de_negocios.transacao_bancaria.exceptions import (
    ErroAoCadastrarTransacaoBancaria,
    ValorDaTransacaoNegativo,
)
from contextos_de_negocios.transacao_bancaria.models import TransacaoBancaria
from contextos_de_negocios.transacao_bancaria.repositorio import (
    RepoTransacaoBancariaEscrita,
)
from contextos_de_negocios.transacao_bancaria.schemas import (
    CadastrarTransacaoBancaria,
)


class TransacaoBancariaControllers:
    @staticmethod
    async def cadastrar(
        session: AsyncSession,
        transacao_bancaria: CadastrarTransacaoBancaria,
    ) -> TransacaoBancaria:
        if transacao_bancaria.valor < 0:
            raise ValorDaTransacaoNegativo

        conta_origem = await RepoContaBancariaLeitura.consultar_por_numero_da_conta(
            session=session, numero_da_conta=transacao_bancaria.numero_da_conta
        )
        if not conta_origem:
            raise ContaBancariaNaoEncontrado

        if transacao_bancaria.numero_da_conta_destino:
            conta_destino = (
                await RepoContaBancariaLeitura.consultar_por_numero_da_conta(
                    session=session,
                    numero_da_conta=transacao_bancaria.numero_da_conta_destino,
                )
            )
            if not conta_destino:
                raise ContaBancariaNaoEncontrado

        novo_transacao_bancaria = TransacaoBancaria(**transacao_bancaria.dict())
        novo_transacao_bancaria.tipo = transacao_bancaria.tipo.value
        try:
            novo_transacao_bancaria = await RepoTransacaoBancariaEscrita.adicionar(
                session=session,
                transacao_bancaria=novo_transacao_bancaria,
            )
        except Exception as erro:
            raise ErroAoCadastrarTransacaoBancaria(
                detail=f"Erro ao cadastrar transacao bancaria: {erro}",
            )
        return novo_transacao_bancaria
