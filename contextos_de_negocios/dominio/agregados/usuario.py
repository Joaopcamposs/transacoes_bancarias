from dataclasses import dataclass
from uuid import UUID

from contextos_de_negocios.utils.constantes import pwd_context


@dataclass
class Usuario:
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
        senhas_conferem = pwd_context.verify(secret=senha, hash=self.senha)
        return senhas_conferem

    @staticmethod
    def criptografar_senha(senha: str) -> str:
        senha_criptografada = pwd_context.hash(secret=senha)
        return senha_criptografada
