from datetime import datetime

import pytz


def get_local_time() -> datetime:
    """Retorna a data e hora atual no fuso horário de São Paulo (America/Sao_Paulo)."""
    return datetime.now(pytz.timezone("America/Sao_Paulo"))
