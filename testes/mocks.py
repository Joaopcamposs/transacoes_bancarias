import asyncio
from dataclasses import dataclass
from decimal import Decimal
from random import randint

import pytest
from pydantic import UUID4

from contextos_de_negocios.dominio.agregados.cliente import Cliente
from contextos_de_negocios.dominio.agregados.conta_bancaria import Conta
from contextos_de_negocios.dominio.agregados.transacao_bancaria import Transacao
from contextos_de_negocios.dominio.entidades.cliente import CadastrarCliente
from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    CadastrarTransacaoBancaria,
)
from contextos_de_negocios.dominio.objetos_de_valor.transacao_bancaria import (
    TipoTransacao,
)
from contextos_de_negocios.servicos.executores.cliente import cadastrar_cliente

from contextos_de_negocios.dominio.entidades.conta_bancaria import (
    CadastrarContaBancaria,
)
from contextos_de_negocios.servicos.executores.conta_bancaria import cadastrar_conta
from contextos_de_negocios.servicos.executores.seguranca import criar_token
from contextos_de_negocios.servicos.executores.transacao_bancaria import (
    cadastrar_transacao_bancaria,
)
from contextos_de_negocios.utils.tipos_basicos import CPF
from libs.ddd.adaptadores.visualizadores import Filtros


@dataclass
class MockUsuarioAPI:
    nome: str
    email: str
    senha: str
    adm: bool
    ativo: bool
    token: str
    id: UUID4 | None = None


def _get_or_create_event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


@pytest.fixture(scope="function")
def mock_usuario_api() -> MockUsuarioAPI:
    from contextos_de_negocios.dominio.entidades.usuario import (
        CadastrarUsuario,
    )
    from contextos_de_negocios.repositorio.repo_consulta.usuario import (
        UsuarioRepoConsulta,
    )
    from contextos_de_negocios.servicos.executores.usuario import cadastrar_usuario
    from sqlalchemy.exc import IntegrityError

    async def _create():
        novo_usuario = CadastrarUsuario(
            nome="Admin",
            email="admin@email.com",
            senha="1234",
            adm=True,
            ativo=True,
        )

        usuario_cadastrado = None
        usuarios_existentes = await UsuarioRepoConsulta().consultar_por_filtros(
            Filtros({})
        )
        if len(list(usuarios_existentes)) == 0:
            try:
                usuario_cadastrado = await cadastrar_usuario(novo_usuario)
            except IntegrityError:
                pass

        if not usuario_cadastrado:
            usuario_cadastrado = await UsuarioRepoConsulta().consultar_um_por_filtros(
                Filtros({"email": novo_usuario.email})
            )

        access_token = criar_token(data={"sub": usuario_cadastrado.email})

        return MockUsuarioAPI(
            id=usuario_cadastrado.id,
            nome=usuario_cadastrado.nome,
            email=usuario_cadastrado.email,
            senha=novo_usuario.senha,
            adm=usuario_cadastrado.adm,
            ativo=usuario_cadastrado.ativo,
            token=access_token,
        )

    loop = _get_or_create_event_loop()
    return loop.run_until_complete(_create())


@pytest.fixture(scope="function")
def mock_cliente_gen() -> dict:
    return {"nome": "Cliente Teste", "cpf": CPF.gerar()}


@pytest.fixture(scope="function")
def mock_cliente(mock_cliente_gen) -> Cliente:
    async def _create():
        dados_para_cadastrar = CadastrarCliente(**mock_cliente_gen)
        cliente = await cadastrar_cliente(cliente=dados_para_cadastrar)
        return cliente

    loop = _get_or_create_event_loop()
    return loop.run_until_complete(_create())


@pytest.fixture(scope="function")
def mock_conta_bancaria_gen() -> dict:
    return {
        "numero_da_conta": "1234",
        "saldo": "0.00",
        "cpf_cliente": CPF.gerar(),
    }


@pytest.fixture(scope="function")
def mock_conta_bancaria(mock_cliente):
    def _create_mock_conta(
        numero_da_conta: str | None = None, saldo: Decimal | None = None
    ) -> Conta:
        async def _async_create():
            dados_para_cadastrar = CadastrarContaBancaria(
                numero_da_conta=numero_da_conta or str(randint(100000, 999999)),
                saldo=saldo or Decimal(0.0),
                cpf_cliente=mock_cliente.cpf,
            )
            conta = await cadastrar_conta(conta_bancaria=dados_para_cadastrar)
            return conta

        loop = _get_or_create_event_loop()
        return loop.run_until_complete(_async_create())

    return _create_mock_conta


@pytest.fixture(scope="function")
def mock_usuario_gen() -> dict:
    return {
        "nome": "Usuário Teste",
        "email": "joao@email.com",
        "senha": "1234",
        "adm": False,
        "ativo": True,
    }


@pytest.fixture(scope="function")
def mock_transacao_bancaria_gen(mock_conta_bancaria_gen) -> dict:
    return {
        "tipo": "deposito",
        "valor": "100.00",
        "numero_da_conta": mock_conta_bancaria_gen["numero_da_conta"],
    }


@pytest.fixture(scope="function")
def mock_transacao_bancaria(mock_conta_bancaria, mock_transacao_bancaria_gen):
    def _create_mock_transacao(
        tipo: str = mock_transacao_bancaria_gen["tipo"],
        valor: Decimal = Decimal(mock_transacao_bancaria_gen["valor"]),
        numero_da_conta: str = mock_transacao_bancaria_gen["numero_da_conta"],
        numero_da_conta_destino: str = "",
    ) -> Transacao:
        async def _async_create():
            dados_para_cadastrar = CadastrarTransacaoBancaria(
                tipo=TipoTransacao[tipo.upper()],
                valor=valor,
                numero_da_conta=numero_da_conta,
                numero_da_conta_destino=numero_da_conta_destino,
            )
            transacao = await cadastrar_transacao_bancaria(
                transacao_bancaria=dados_para_cadastrar
            )
            return transacao

        loop = _get_or_create_event_loop()
        return loop.run_until_complete(_async_create())

    return _create_mock_transacao
