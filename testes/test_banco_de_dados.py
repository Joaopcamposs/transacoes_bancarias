import os

from contextos_de_negocios.utils.constantes import POSTGRES_TESTE
from infra.banco_de_dados import obter_uri_do_banco_de_dados


def test_obter_uri_teste():
    os.environ["TEST_ENV"] = "true"
    uri = obter_uri_do_banco_de_dados()
    assert uri == POSTGRES_TESTE


def test_obter_uri_producao():
    os.environ["TEST_ENV"] = "false"
    uri = obter_uri_do_banco_de_dados()
    assert "postgresql+asyncpg" in uri
