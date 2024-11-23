# noinspection PyUnresolvedReferences
def start_mappers():
    """Apenas importando, todos os mapeamentos são realizados"""
    from infra.banco_de_dados import mapper_registry as mapper_registry

    # if mapper_registry.mappers:
    #     return  # Retorna imediatamente se os mapeadores já foram configurados

    from contextos_de_negocios.repositorio.orm.imperativo.usuario import (
        usuario_mapper as usuario_mapper,
    )
    from contextos_de_negocios.repositorio.orm.imperativo.cliente import (
        cliente_mapper as cliente_mapper,
    )
    from contextos_de_negocios.repositorio.orm.imperativo.conta_bancaria import (
        conta_mapper as conta_mapper,
    )
    from contextos_de_negocios.repositorio.orm.imperativo.transacao_bancaria import (
        transacao_bancaria_mapper as transacao_bancaria_mapper,
    )
