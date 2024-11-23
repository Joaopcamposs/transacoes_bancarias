from dataclasses import dataclass


@dataclass
class Agregado:
    def to_dict(self) -> dict:
        dados = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
        tipo_para_nao_converter = (str, int, float, bool, dict, list, tuple)
        dados_convertidos = {
            key: str(value) if type(value) not in tipo_para_nao_converter else value
            for key, value in dados.items()
        }
        return dados_convertidos
