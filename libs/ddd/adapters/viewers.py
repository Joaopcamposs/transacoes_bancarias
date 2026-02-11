from typing import Any


class Filters(dict):
    """
    Classe base para filtros genéricos.
    Converte automaticamente os campos não nulos em um dicionário utilizável para consultas.
    """

    def __init__(self, filters: dict[str, Any]) -> None:
        """Inicializa os filtros removendo valores nulos."""
        super().__init__()
        self.update(self.to_query(filters))

    def __new__(cls, *args: Any, **kwargs: Any) -> "Filters":
        """Cria uma nova instância de Filters."""
        return super().__new__(cls)

    @staticmethod
    def to_query(filters: dict[str, Any]) -> dict[str, Any]:
        """Retorna um dicionário contendo somente os campos não nulos."""
        return {key: value for key, value in filters.items() if value is not None}

    def __str__(self) -> str:
        """Retorna a representação em string dos filtros."""
        return str(dict(self))
