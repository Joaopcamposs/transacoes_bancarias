from pydantic import BaseModel


class Token(BaseModel):
    """Modelo de resposta contendo o token de acesso JWT."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Modelo de dados extraídos do token JWT."""

    email: str | None = None
