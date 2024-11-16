from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession

from contextos_de_negocios.dominio.exceptions import (
    ClienteNaoEncontrado,
    ContaBancariaNaoEncontrado,
    ContaBancariaJaCadastrado,
)
from contextos_de_negocios.repositorio.repo_consulta.cliente import ClienteRepoConsulta
from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
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


async def cadastrar_conta(
    session: AsyncSession,
    conta_bancaria: CadastrarContaBancaria,
) -> Conta:
    conta_bancaria_com_mesmo_numero = await ContaBancariaRepoConsulta(
        session=session
    ).consultar_um_por_filtros(
        Filtros({"numero_da_conta": conta_bancaria.numero_da_conta})
    )
    if conta_bancaria_com_mesmo_numero:
        raise ContaBancariaJaCadastrado

    # Verifica se o CPF existe
    cliente = await ClienteRepoConsulta(session=session).consultar_um_por_filtros(
        Filtros({"cpf": conta_bancaria.cpf_cliente})
    )
    if not cliente:
        raise ClienteNaoEncontrado

    nova_conta_bancaria = Conta.retornar_agregado_para_cadastro(
        numero_da_conta=conta_bancaria.numero_da_conta,
        saldo=conta_bancaria.saldo,
        cpf_cliente=conta_bancaria.cpf_cliente,
    )

    id_resultado = await ContaBancariaRepoDominio(session=session).adicionar(
        conta=nova_conta_bancaria,
        tipo_operacao=TipoOperacao.INSERCAO,
    )
    nova_conta_bancaria.id = id_resultado

    return nova_conta_bancaria


async def atualizar_conta(
    session: AsyncSession,
    conta_bancaria_att: AtualizarContaBancaria,
) -> Conta:
    conta = await ContaBancariaRepoDominio(
        session=session
    ).consultar_por_numero_da_conta(
        numero_da_conta=conta_bancaria_att._numero_da_conta_antigo
    )

    if not conta:
        raise ContaBancariaNaoEncontrado

    conta.atualizar(
        numero_da_conta=conta_bancaria_att.numero_da_conta,
        cpf_cliente=conta_bancaria_att.cpf_cliente,
    )

    await ContaBancariaRepoDominio(session=session).adicionar(
        conta=conta,
        tipo_operacao=TipoOperacao.ATUALIZACAO,
    )

    return conta


async def remover_conta(session: AsyncSession, id: Uuid) -> str:
    conta = await ContaBancariaRepoDominio(session=session).consultar_por_id(id=id)

    if not conta:
        raise ContaBancariaNaoEncontrado

    await ContaBancariaRepoDominio(session=session).remover(conta=conta)

    return "Conta Bancaria deletada!"
