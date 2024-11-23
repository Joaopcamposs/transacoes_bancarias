from sqlalchemy import Uuid

from contextos_de_negocios.dominio.agregados.cliente import Cliente
from contextos_de_negocios.dominio.exceptions import (
    ClienteJaCadastrado,
    ClienteNaoEncontrado,
)
from contextos_de_negocios.repositorio.repo_consulta.cliente import (
    ClienteRepoConsulta,
)
from contextos_de_negocios.repositorio.repo_dominio.cliente import ClienteRepoDominio
from contextos_de_negocios.dominio.entidades.cliente import (
    CadastrarCliente,
    AtualizarCliente,
)
from contextos_de_negocios.utils.tipos_basicos import TipoOperacao, CPF
from libs.ddd.adaptadores.visualizadores import Filtros


async def cadastrar_cliente(
    cliente: CadastrarCliente,
) -> Cliente:
    cliente_com_mesmo_cpf = await ClienteRepoConsulta().consultar_um_por_filtros(
        Filtros({"cpf": cliente.cpf})
    )

    if cliente_com_mesmo_cpf:
        raise ClienteJaCadastrado

    novo_cliente = Cliente.retornar_agregado_para_cadastro(
        nome=cliente.nome,
        cpf=CPF(cliente.cpf),
    )
    id_resultado = await ClienteRepoDominio().adicionar(
        cliente=novo_cliente,
        tipo_operacao=TipoOperacao.INSERCAO,
    )
    novo_cliente.id = id_resultado

    return novo_cliente


async def atualizar_cliente(cliente_att: AtualizarCliente) -> Cliente:
    cliente = await ClienteRepoDominio().consultar_por_id(id=cliente_att._id)

    if not cliente:
        raise ClienteNaoEncontrado

    cliente.atualizar(nome=cliente_att.nome, cpf=CPF(cliente_att.cpf))

    await ClienteRepoDominio().adicionar(
        cliente=cliente, tipo_operacao=TipoOperacao.ATUALIZACAO
    )
    return cliente


async def remover_cliente(id: Uuid) -> str:
    cliente = await ClienteRepoDominio().consultar_por_id(id=id)

    if not cliente:
        raise ClienteNaoEncontrado

    await ClienteRepoDominio().remover(cliente=cliente)

    return "Cliente deletado!"
