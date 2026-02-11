from dataclasses import dataclass
from typing import Any


@dataclass
class Aggregate:
    """Classe base para agregados do domínio, seguindo o padrão DDD."""

    def to_dict(self) -> dict[str, Any]:
        """Converte o agregado em um dicionário, excluindo atributos privados."""
        data = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
        types_to_skip = (str, int, float, bool, dict, list, tuple)
        converted_data = {
            key: str(value) if type(value) not in types_to_skip else value
            for key, value in data.items()
        }
        return converted_data
