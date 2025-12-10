from dataclasses import dataclass
from uuid import UUID

import bcrypt

from libs.ddd.dominio.agregado import Agregado


@dataclass
class Usuario(Agregado):
    nome: str
    email: str
    senha: str
    adm: bool
    ativo: bool
    id: UUID | None = None

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        nome: str,
        email: str,
        senha: str,
        adm: bool,
        ativo: bool,
        criptografar_senha: bool = True,
    ) -> "Usuario":
        if criptografar_senha:
            senha = cls.criptografar_senha(senha)
        email = email.lower()
        return Usuario(nome=nome, email=email, senha=senha, adm=adm, ativo=ativo)

    def cadastrar(self) -> None: ...

    def atualizar(
        self, nome: str, email: str, senha: str, adm: bool, ativo: bool
    ) -> None:
        self.nome = nome
        self.email = email
        self.senha = senha
        self.adm = adm
        self.ativo = ativo

    def remover(self) -> None: ...

    def verificar_senha(self, senha: str) -> bool:
        return bcrypt.checkpw(senha.encode()[:72], self.senha.encode())

    @staticmethod
    def criptografar_senha(senha: str) -> str:
        return bcrypt.hashpw(senha.encode()[:72], bcrypt.gensalt()).decode()
