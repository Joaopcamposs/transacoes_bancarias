from dataclasses import dataclass
from decimal import Decimal
from random import randint

import pytest
import pytest_asyncio
from pydantic import UUID4

from contextos_de_negocios.repositorio.orm.cliente import Cliente
from contextos_de_negocios.dominio.entidades.cliente import CadastrarCliente
from contextos_de_negocios.servicos.executores.cliente import cadastrar_cliente
from contextos_de_negocios.servicos.executores.conta_bancaria import (
    ContaBancariaControllers,
)
from contextos_de_negocios.repositorio.orm.conta_bancaria import ContaBancaria
from contextos_de_negocios.dominio.entidades.conta_bancaria import (
    CadastrarContaBancaria,
)
from contextos_de_negocios.servicos.executores.seguranca import Seguranca
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


@pytest_asyncio.fixture(scope="function")
async def mock_usuario_api(session_factory) -> MockUsuarioAPI:
    from contextos_de_negocios.dominio.entidades.usuario import (
        CadastrarUsuario,
    )
    from contextos_de_negocios.repositorio.repo_consulta.usuario import (
        UsuarioRepoConsulta,
    )
    from contextos_de_negocios.servicos.executores.usuario import cadastrar_usuario

    async with session_factory() as session:
        novo_usuario = CadastrarUsuario(
            nome="Admin",
            email="admin@email.com",
            senha="1234",
            adm=True,
            ativo=True,
        )

        usuario_cadastrado = None
        if (
            len(
                list(
                    await UsuarioRepoConsulta(session=session).consultar_por_filtros(
                        Filtros({})
                    )
                )
            )
            == 0
        ):
            usuario_cadastrado = await cadastrar_usuario(session, novo_usuario)
            print(usuario_cadastrado)

        if not usuario_cadastrado:
            usuario_cadastrado = await UsuarioRepoConsulta(
                session=session
            ).consultar_um_por_filtros(Filtros({"email": novo_usuario.email}))

        access_token = Seguranca.criar_token(data={"sub": usuario_cadastrado.email})

        usuario_mock = MockUsuarioAPI(
            id=usuario_cadastrado.id,
            nome=usuario_cadastrado.nome,
            email=usuario_cadastrado.email,
            senha=novo_usuario.senha,
            adm=usuario_cadastrado.adm,
            ativo=usuario_cadastrado.ativo,
            token=access_token,
        )

        return usuario_mock


@pytest.fixture(scope="function")
def mock_cliente_gen() -> dict:
    return {"nome": "Cliente Teste", "cpf": CPF.gerar()}


@pytest_asyncio.fixture(scope="function")
async def mock_cliente(mock_cliente_gen, session_factory) -> Cliente:
    dados_para_cadastrar = CadastrarCliente(**mock_cliente_gen)
    async with session_factory() as session:
        cliente = await cadastrar_cliente(session=session, cliente=dados_para_cadastrar)

    return cliente


@pytest.fixture(scope="function")
def mock_conta_bancaria_gen() -> dict:
    return {
        "numero_da_conta": "1234",
        "saldo": "0.00",
        "cpf_cliente": CPF.gerar(),
    }


@pytest_asyncio.fixture(scope="function")
async def mock_conta_bancaria(mock_cliente, session_factory):
    async def _create_mock_conta(
        numero_da_conta: str | None = None, saldo: Decimal | None = None
    ) -> ContaBancaria:
        dados_para_cadastrar = CadastrarContaBancaria(
            numero_da_conta=numero_da_conta or str(randint(100000, 999999)),
            saldo=saldo or Decimal(0.0),
            cpf_cliente=mock_cliente.cpf,
        )
        async with session_factory() as session:
            conta = await ContaBancariaControllers.cadastrar(
                session=session, conta_bancaria=dados_para_cadastrar
            )
        return conta

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
