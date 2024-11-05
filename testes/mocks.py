from dataclasses import dataclass
from decimal import Decimal
from random import randint

import pytest
import pytest_asyncio
from pydantic import UUID4

from contextos_de_negocios.cliente.controllers import ClienteControllers
from contextos_de_negocios.cliente.models import Cliente
from contextos_de_negocios.cliente.schemas import CadastrarEAtualizarCliente
from contextos_de_negocios.conta_bancaria.controllers import ContaBancariaControllers
from contextos_de_negocios.conta_bancaria.models import ContaBancaria
from contextos_de_negocios.conta_bancaria.schemas import CadastrarContaBancaria
from contextos_de_negocios.servicos.controllers import Servicos
from contextos_de_negocios.utils.tipos_basicos import CPF


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
    usuario_mock = MockUsuarioAPI(
        nome="Admin",
        email="admin@email.com",
        senha="1234",
        adm=True,
        ativo=True,
        token="",
    )

    usuario_mock.senha = Servicos.criptografar_senha(usuario_mock.senha)

    from contextos_de_negocios.usuario.schemas import CadastrarEAtualizarUsuario
    from contextos_de_negocios.usuario.repositorio import RepoUsuarioLeitura
    from contextos_de_negocios.usuario.controllers import UsuarioControllers

    async with session_factory() as session:
        novo_usuario = CadastrarEAtualizarUsuario(
            nome=usuario_mock.nome,
            email=usuario_mock.email,
            senha=usuario_mock.senha,
            adm=usuario_mock.adm,
            ativo=usuario_mock.ativo,
        )

        usuario_cadastrado = None
        if len(list(await RepoUsuarioLeitura.consultar_todos(session))) == 0:
            usuario_cadastrado = await UsuarioControllers.cadastrar(
                session, novo_usuario
            )
            print(usuario_cadastrado)

        if not usuario_cadastrado:
            usuario_cadastrado = await RepoUsuarioLeitura.consultar_por_email(
                session, novo_usuario.email
            )

        access_token = Servicos.criar_token(data={"sub": usuario_cadastrado.email})

        usuario_mock.id = str(usuario_cadastrado.id)
        usuario_mock.token = access_token

        return usuario_mock


@pytest.fixture(scope="function")
def mock_cliente_gen() -> dict:
    return {"nome": "Cliente Teste", "cpf": CPF().gerar()}


@pytest_asyncio.fixture(scope="function")
async def mock_cliente(mock_cliente_gen, session_factory) -> Cliente:
    dados_para_cadastrar = CadastrarEAtualizarCliente(**mock_cliente_gen)
    async with session_factory() as session:
        cliente = await ClienteControllers.cadastrar(
            session=session, cliente=dados_para_cadastrar
        )

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
