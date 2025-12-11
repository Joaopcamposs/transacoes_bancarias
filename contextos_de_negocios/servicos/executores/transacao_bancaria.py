from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.exceptions import ContaBancariaNaoEncontrado
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
)


async def cadastrar_transacao_bancaria(
    transacao_bancaria: CadastrarTransacaoBancaria,
) -> Transacao:
    from libs.ddd.adaptadores.unit_of_work import SqlAlchemyUnitOfWork
    from contextos_de_negocios.utils.tipos_basicos import TipoOperacao
    from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
        TipoTransacao,
    )

    async with SqlAlchemyUnitOfWork() as uow:
        # Ordenar bloqueios para evitar Deadlocks
        contas_para_bloquear = [transacao_bancaria.numero_da_conta]
        if transacao_bancaria.numero_da_conta_destino:
            contas_para_bloquear.append(transacao_bancaria.numero_da_conta_destino)
        contas_para_bloquear.sort()

        mapa_contas = {}
        for numero in contas_para_bloquear:
            conta = await uow.contas.consultar_por_numero_da_conta(
                numero_da_conta=numero, lock=True
            )
            if conta:
                mapa_contas[numero] = conta

        conta_origem = mapa_contas.get(transacao_bancaria.numero_da_conta)
        if not conta_origem:
            raise ContaBancariaNaoEncontrado

        conta_destino = None
        if transacao_bancaria.numero_da_conta_destino:
            conta_destino = mapa_contas.get(transacao_bancaria.numero_da_conta_destino)
            if not conta_destino:
                raise ContaBancariaNaoEncontrado

        novo_transacao_bancaria = conta_origem.nova_transacao(transacao_bancaria)

        if transacao_bancaria.tipo == TipoTransacao.TRANSFERENCIA and conta_destino:
            # Atualiza saldo da conta destino em memória
            conta_destino.realizar_deposito(transacao_bancaria.valor)
            # Persiste atualização
            await uow.contas.adicionar(conta_destino, TipoOperacao.ATUALIZACAO)

        # Persiste atualização da conta origem
        await uow.contas.adicionar(conta_origem, TipoOperacao.ATUALIZACAO)

        # Persiste a transação
        id_resultado = await uow.transacoes.adicionar(
            transacao=novo_transacao_bancaria,
        )
        novo_transacao_bancaria.id = id_resultado

        await uow.commit()

    return novo_transacao_bancaria
