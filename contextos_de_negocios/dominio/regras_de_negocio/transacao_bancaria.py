from datetime import datetime

import pytz


def obter_hora_local() -> datetime:
    return datetime.now(pytz.timezone("America/Sao_Paulo"))
