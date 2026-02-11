from dataclasses import dataclass
from uuid import UUID

import bcrypt

from libs.ddd.domain.aggregate import Aggregate


@dataclass
class User(Aggregate):
    """Agregado raiz que representa um usuário do sistema."""

    name: str
    email: str
    password: str
    is_admin: bool
    is_active: bool
    id: UUID | None = None

    @classmethod
    def return_aggregate_for_creation(
        cls,
        name: str,
        email: str,
        password: str,
        is_admin: bool,
        is_active: bool,
        encrypt_password: bool = True,
    ) -> "User":
        """Retorna uma instância do agregado User preparada para cadastro."""
        if encrypt_password:
            password = cls.hash_password(password)
        email = email.lower()
        return User(
            name=name,
            email=email,
            password=password,
            is_admin=is_admin,
            is_active=is_active,
        )

    def create(self) -> None:
        """Executa a lógica de criação do usuário."""
        ...

    def update(
        self, name: str, email: str, password: str, is_admin: bool, is_active: bool
    ) -> None:
        """Atualiza os dados do usuário."""
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

    def remove(self) -> None:
        """Executa a lógica de remoção do usuário."""
        ...

    def verify_password(self, password: str) -> bool:
        """Verifica se a senha fornecida corresponde à senha criptografada do usuário."""
        return bcrypt.checkpw(password.encode()[:72], self.password.encode())

    @staticmethod
    def hash_password(password: str) -> str:
        """Criptografa a senha usando bcrypt."""
        return bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt()).decode()
