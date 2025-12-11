"""Mecanismo de lock para garantir concorrência.

Com PostgreSQL, usamos FOR UPDATE que é o mecanismo nativo e mais eficiente.
Este módulo existe apenas para manter compatibilidade da interface.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator


class GerenciadorDeLocks:
    """Gerenciador de locks por conta.

    Com PostgreSQL (produção e testes), o FOR UPDATE cuida da concorrência.
    Este gerenciador apenas mantém a interface para compatibilidade.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @asynccontextmanager
    async def bloquear_contas(self, *numeros_conta: str) -> AsyncGenerator[None, None]:
        """Interface de bloqueio de contas.

        Com PostgreSQL, a concorrência é garantida pelo FOR UPDATE.
        Este métodu existe apenas para manter compatibilidade da interface.
        """
        yield


# Singleton global
gerenciador_locks = GerenciadorDeLocks()
