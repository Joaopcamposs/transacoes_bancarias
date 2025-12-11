import asyncio
from decimal import Decimal

import httpx
import pytest
from httpx import ASGITransport

from contextos_de_negocios.main import app
import infra.banco_de_dados as db_module


def teste_deposito(client_api, mock_usuario_api, mock_conta_bancaria):
    conta = mock_conta_bancaria(saldo="0.00")
    numero = conta["numero_da_conta"]

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "deposito",
            "valor": 100.00,
            "numero_da_conta": numero,
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api.status_code == 200, resposta_api.text

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "100.00"


def teste_saque(client_api, mock_usuario_api, mock_conta_bancaria):
    conta = mock_conta_bancaria(saldo="100.00")
    numero = conta["numero_da_conta"]

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "saque",
            "valor": 50.00,
            "numero_da_conta": numero,
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api.status_code == 200, resposta_api.text

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "50.00"


def teste_transferencia(client_api, mock_usuario_api, mock_conta_bancaria):
    conta1 = mock_conta_bancaria(saldo="50.00")
    conta2 = mock_conta_bancaria(saldo="0.00")
    numero1 = conta1["numero_da_conta"]
    numero2 = conta2["numero_da_conta"]

    resposta_api = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "transferencia",
            "valor": 30.00,
            "numero_da_conta": numero1,
            "numero_da_conta_destino": numero2,
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api.status_code == 200, resposta_api.text

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero1}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "20.00"

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero2}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "30.00"


def teste_concorrencia_deposito_e_saque(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta = mock_conta_bancaria(saldo="50.00")
    numero = conta["numero_da_conta"]

    # Deposito
    resposta_dep = client_api.post(
        "api/transacao_bancaria",
        json={"tipo": "deposito", "valor": 50.00, "numero_da_conta": numero},
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_dep.status_code == 200, resposta_dep.text

    # Saque
    resposta_saque = client_api.post(
        "api/transacao_bancaria",
        json={"tipo": "saque", "valor": 30.00, "numero_da_conta": numero},
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_saque.status_code == 200, resposta_saque.text

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "70.00"


def teste_concorrencia_deposito_e_transferencia(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta1 = mock_conta_bancaria(saldo="100.00")
    conta2 = mock_conta_bancaria(saldo="0.00")
    numero1 = conta1["numero_da_conta"]
    numero2 = conta2["numero_da_conta"]

    # Deposito
    resposta_dep = client_api.post(
        "api/transacao_bancaria",
        json={"tipo": "deposito", "valor": 100.00, "numero_da_conta": numero1},
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_dep.status_code == 200, resposta_dep.text

    # Transferencia
    resposta_transf = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "transferencia",
            "valor": 50.00,
            "numero_da_conta": numero1,
            "numero_da_conta_destino": numero2,
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_transf.status_code == 200, resposta_transf.text

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero1}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "150.00"

    resposta_api_conta_2 = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero2}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta_2.status_code == 200, resposta_api_conta_2.text
    assert resposta_api_conta_2.json()[0]["saldo"] == "50.00"


def teste_concorrencia_transferencias(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    conta1 = mock_conta_bancaria(saldo="100.00")
    conta2 = mock_conta_bancaria(saldo="20.00")
    conta3 = mock_conta_bancaria(saldo="0.00")
    numero1 = conta1["numero_da_conta"]
    numero2 = conta2["numero_da_conta"]
    numero3 = conta3["numero_da_conta"]

    # Transferencia conta1 -> conta2
    resposta1 = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "transferencia",
            "valor": 20.00,
            "numero_da_conta": numero1,
            "numero_da_conta_destino": numero2,
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta1.status_code == 200, resposta1.text

    # Transferencia conta2 -> conta3
    resposta2 = client_api.post(
        "api/transacao_bancaria",
        json={
            "tipo": "transferencia",
            "valor": 10.00,
            "numero_da_conta": numero2,
            "numero_da_conta_destino": numero3,
        },
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta2.status_code == 200, resposta2.text

    resposta_api_conta = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero1}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta.status_code == 200, resposta_api_conta.text
    assert resposta_api_conta.json()[0]["saldo"] == "80.00"

    resposta_api_conta_2 = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero2}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta_2.status_code == 200, resposta_api_conta_2.text
    assert resposta_api_conta_2.json()[0]["saldo"] == "30.00"

    resposta_api_conta_3 = client_api.get(
        f"api/conta_bancarias?numero_da_conta={numero3}",
        headers={"Authorization": f"Bearer {mock_usuario_api.token}"},
    )
    assert resposta_api_conta_3.status_code == 200, resposta_api_conta_3.text
    assert resposta_api_conta_3.json()[0]["saldo"] == "10.00"


# =============================================================================
# TESTES DE CONSISTÊNCIA DE SALDO (OPERAÇÕES MÚLTIPLAS)
# =============================================================================


def fazer_transacao(
    client,
    token: str,
    tipo: str,
    valor: float,
    numero_da_conta: str,
    numero_da_conta_destino: str | None = None,
) -> dict:
    """Faz uma requisição de transação."""
    corpo = {"tipo": tipo, "valor": valor, "numero_da_conta": numero_da_conta}
    if numero_da_conta_destino:
        corpo["numero_da_conta_destino"] = numero_da_conta_destino
    resposta = client.post(
        "api/transacao_bancaria",
        json=corpo,
        headers={"Authorization": f"Bearer {token}"},
    )
    return {
        "status_code": resposta.status_code,
        "body": resposta.json() if resposta.status_code < 500 else resposta.text,
    }


def obter_saldo(client, token: str, numero_da_conta: str) -> Decimal:
    """Obtém o saldo de uma conta."""
    resposta = client.get(
        f"api/conta_bancarias?numero_da_conta={numero_da_conta}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resposta.status_code == 200 and resposta.json():
        return Decimal(resposta.json()[0]["saldo"])
    return Decimal("0.00")


def teste_consistencia_depositos_multiplos(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    """Teste de consistência: N depósitos na mesma conta.

    Valida que a soma de todos os depósitos é refletida corretamente no saldo final.
    """
    NUMERO_DEPOSITOS = 20
    VALOR_DEPOSITO = Decimal("10.00")
    SALDO_INICIAL = Decimal("0.00")

    conta = mock_conta_bancaria(saldo=str(SALDO_INICIAL))
    numero_conta = conta["numero_da_conta"]
    token = mock_usuario_api.token

    resultados = [
        fazer_transacao(
            client_api, token, "deposito", float(VALOR_DEPOSITO), numero_conta
        )
        for _ in range(NUMERO_DEPOSITOS)
    ]
    sucessos = sum(1 for r in resultados if r["status_code"] == 200)

    saldo_final = obter_saldo(client_api, token, numero_conta)
    saldo_esperado = SALDO_INICIAL + (VALOR_DEPOSITO * sucessos)

    # INVARIANTE: Saldo deve ser exatamente a soma dos depósitos bem sucedidos
    assert saldo_final == saldo_esperado, (
        f"Saldo inconsistente! Final: {saldo_final}, Esperado: {saldo_esperado}. "
        f"Depósitos OK: {sucessos}/{NUMERO_DEPOSITOS}"
    )


def teste_consistencia_saques_multiplos(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    """Teste de consistência: N saques com saldo limitado.

    Garante que não ocorra saldo negativo.
    """
    NUMERO_SAQUES = 15
    VALOR_SAQUE = Decimal("10.00")
    SALDO_INICIAL = Decimal("50.00")  # Permite apenas 5 saques com sucesso

    conta = mock_conta_bancaria(saldo=str(SALDO_INICIAL))
    numero_conta = conta["numero_da_conta"]
    token = mock_usuario_api.token

    resultados = [
        fazer_transacao(client_api, token, "saque", float(VALOR_SAQUE), numero_conta)
        for _ in range(NUMERO_SAQUES)
    ]
    sucessos = sum(1 for r in resultados if r["status_code"] == 200)

    saldo_final = obter_saldo(client_api, token, numero_conta)
    saldo_esperado = SALDO_INICIAL - (VALOR_SAQUE * sucessos)

    # INVARIANTE CRÍTICO: Saldo nunca pode ser negativo
    assert saldo_final >= Decimal("0.00"), (
        f"ERRO CRÍTICO: Saldo negativo detectado! Saldo: {saldo_final}"
    )

    # Verificar consistência
    assert saldo_final == saldo_esperado, (
        f"Saldo inconsistente! Final: {saldo_final}, Esperado: {saldo_esperado}. "
        f"Saques OK: {sucessos}/{NUMERO_SAQUES}"
    )

    # Máximo de saques bem sucedidos deve ser 5 (50/10)
    assert sucessos <= 5, f"Mais saques que o permitido: {sucessos}"


def teste_consistencia_depositos_e_saques_intercalados(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    """Teste de consistência: depósitos e saques intercalados.

    Valida que o saldo final é consistente.
    """
    SALDO_INICIAL = Decimal("100.00")
    NUM_DEPOSITOS = 10
    NUM_SAQUES = 10
    VALOR_DEPOSITO = Decimal("20.00")
    VALOR_SAQUE = Decimal("15.00")

    conta = mock_conta_bancaria(saldo=str(SALDO_INICIAL))
    numero_conta = conta["numero_da_conta"]
    token = mock_usuario_api.token

    resultados_depositos = []
    resultados_saques = []

    # Intercalar operações
    for i in range(max(NUM_DEPOSITOS, NUM_SAQUES)):
        if i < NUM_DEPOSITOS:
            resultados_depositos.append(
                fazer_transacao(
                    client_api, token, "deposito", float(VALOR_DEPOSITO), numero_conta
                )
            )
        if i < NUM_SAQUES:
            resultados_saques.append(
                fazer_transacao(
                    client_api, token, "saque", float(VALOR_SAQUE), numero_conta
                )
            )

    sucessos_depositos = sum(1 for r in resultados_depositos if r["status_code"] == 200)
    sucessos_saques = sum(1 for r in resultados_saques if r["status_code"] == 200)

    saldo_final = obter_saldo(client_api, token, numero_conta)
    saldo_esperado = (
        SALDO_INICIAL
        + (VALOR_DEPOSITO * sucessos_depositos)
        - (VALOR_SAQUE * sucessos_saques)
    )

    # INVARIANTE: Saldo nunca negativo
    assert saldo_final >= Decimal("0.00"), f"Saldo negativo: {saldo_final}"

    # Verificar consistência
    assert saldo_final == saldo_esperado, (
        f"Saldo inconsistente! Final: {saldo_final}, Esperado: {saldo_esperado}. "
        f"Depósitos OK: {sucessos_depositos}, Saques OK: {sucessos_saques}"
    )


def teste_consistencia_transferencias_bidirecionais(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    """Teste de consistência: transferências A→B e B→A.

    Valida que a soma total é conservada.
    """
    SALDO_INICIAL = Decimal("100.00")
    NUM_TRANSFERENCIAS_POR_DIRECAO = 5
    VALOR_TRANSFERENCIA = Decimal("10.00")

    conta_a = mock_conta_bancaria(saldo=str(SALDO_INICIAL))
    conta_b = mock_conta_bancaria(saldo=str(SALDO_INICIAL))
    numero_a = conta_a["numero_da_conta"]
    numero_b = conta_b["numero_da_conta"]
    token = mock_usuario_api.token

    resultados_ab = []
    resultados_ba = []

    # Intercalar transferências
    for _ in range(NUM_TRANSFERENCIAS_POR_DIRECAO):
        resultados_ab.append(
            fazer_transacao(
                client_api,
                token,
                "transferencia",
                float(VALOR_TRANSFERENCIA),
                numero_a,
                numero_b,
            )
        )
        resultados_ba.append(
            fazer_transacao(
                client_api,
                token,
                "transferencia",
                float(VALOR_TRANSFERENCIA),
                numero_b,
                numero_a,
            )
        )

    sucessos_ab = sum(1 for r in resultados_ab if r["status_code"] == 200)
    sucessos_ba = sum(1 for r in resultados_ba if r["status_code"] == 200)

    saldo_a = obter_saldo(client_api, token, numero_a)
    saldo_b = obter_saldo(client_api, token, numero_b)

    # INVARIANTE: Soma total deve ser conservada
    soma_total = saldo_a + saldo_b
    soma_esperada = SALDO_INICIAL * 2

    assert soma_total == soma_esperada, (
        f"ERRO: Soma não conservada! Total: {soma_total}, Esperado: {soma_esperada}. "
        f"Saldo A: {saldo_a}, Saldo B: {saldo_b}. "
        f"Transferências A→B: {sucessos_ab}, B→A: {sucessos_ba}"
    )

    # Verificar consistência individual
    delta_esperado_a = VALOR_TRANSFERENCIA * (sucessos_ba - sucessos_ab)
    saldo_esperado_a = SALDO_INICIAL + delta_esperado_a

    assert saldo_a == saldo_esperado_a, (
        f"Saldo A inconsistente: {saldo_a} != {saldo_esperado_a}"
    )


def teste_consistencia_alta_carga(client_api, mock_usuario_api, mock_conta_bancaria):
    """Teste de stress: alta carga de operações.

    Simula cenário com muitas operações.
    """
    SALDO_INICIAL = Decimal("10000.00")
    NUM_CONTAS = 3
    NUM_OPERACOES_POR_CONTA = 5
    VALOR_DEPOSITO = Decimal("50.00")
    VALOR_SAQUE = Decimal("30.00")

    # Criar contas
    numeros = [
        mock_conta_bancaria(saldo=str(SALDO_INICIAL))["numero_da_conta"]
        for _ in range(NUM_CONTAS)
    ]
    token = mock_usuario_api.token
    soma_inicial_total = SALDO_INICIAL * NUM_CONTAS

    resultados = []

    # Operações de depósito e saque para cada conta
    for numero in numeros:
        for _ in range(NUM_OPERACOES_POR_CONTA):
            resultados.append(
                fazer_transacao(
                    client_api, token, "deposito", float(VALOR_DEPOSITO), numero
                )
            )
            resultados.append(
                fazer_transacao(client_api, token, "saque", float(VALOR_SAQUE), numero)
            )

    # Adicionar algumas transferências
    resultados.append(
        fazer_transacao(
            client_api, token, "transferencia", 25.00, numeros[0], numeros[1]
        )
    )
    resultados.append(
        fazer_transacao(
            client_api, token, "transferencia", 25.00, numeros[1], numeros[2]
        )
    )

    # Verificar saldos finais
    saldos_finais = {
        numero: obter_saldo(client_api, token, numero) for numero in numeros
    }

    # INVARIANTE CRÍTICO: Nenhum saldo negativo
    for numero, saldo in saldos_finais.items():
        assert saldo >= Decimal("0.00"), f"Saldo negativo em {numero}: {saldo}"

    # Contar operações bem sucedidas por tipo
    depositos_ok = saques_ok = transferencias_ok = 0
    for r in resultados:
        if r["status_code"] == 200:
            body = r["body"]
            if isinstance(body, dict):
                tipo = body.get("tipo", "")
                if tipo == "deposito":
                    depositos_ok += 1
                elif tipo == "saque":
                    saques_ok += 1
                elif tipo == "transferencia":
                    transferencias_ok += 1

    # Verificar que houve operações bem sucedidas
    total_operacoes_ok = depositos_ok + saques_ok + transferencias_ok
    assert total_operacoes_ok > 0, "Nenhuma operação teve sucesso"

    # Verificar soma total (transferências não alteram soma)
    soma_final = sum(saldos_finais.values())
    soma_esperada = (
        soma_inicial_total + (VALOR_DEPOSITO * depositos_ok) - (VALOR_SAQUE * saques_ok)
    )

    assert soma_final == soma_esperada, (
        f"Soma inconsistente! Final: {soma_final}, Esperado: {soma_esperada}. "
        f"Depósitos: {depositos_ok}, Saques: {saques_ok}, Transferências: {transferencias_ok}"
    )


def teste_consistencia_race_condition_saldo_insuficiente(
    client_api, mock_usuario_api, mock_conta_bancaria
):
    """Teste de validação de saldo: múltiplos saques com saldo justo.

    Valida que apenas 1 saque do saldo é permitido.
    """
    SALDO_INICIAL = Decimal("100.00")
    VALOR_SAQUE = Decimal("100.00")  # Cada saque consome o saldo inteiro
    NUM_SAQUES = 10  # Apenas 1 deve ter sucesso

    conta = mock_conta_bancaria(saldo=str(SALDO_INICIAL))
    numero_conta = conta["numero_da_conta"]
    token = mock_usuario_api.token

    resultados = [
        fazer_transacao(client_api, token, "saque", float(VALOR_SAQUE), numero_conta)
        for _ in range(NUM_SAQUES)
    ]
    sucessos = sum(1 for r in resultados if r["status_code"] == 200)
    saldo_final = obter_saldo(client_api, token, numero_conta)

    # INVARIANTE CRÍTICO: Saldo NUNCA pode ser negativo
    assert saldo_final >= Decimal("0.00"), f"Saldo negativo: {saldo_final}"

    # Apenas 1 saque deve ter sucesso (validação sequencial)
    assert sucessos == 1, (
        f"Esperado 1 sucesso, obteve {sucessos}. Saldo final: {saldo_final}"
    )

    assert saldo_final == Decimal("0.00"), (
        f"Saldo final deveria ser 0.00, mas é {saldo_final}"
    )


# =============================================================================
# TESTES DE CONCORRÊNCIA REAL COM ASYNCIO
# =============================================================================


async def fazer_transacao_async(
    client: httpx.AsyncClient,
    token: str,
    tipo: str,
    valor: float,
    numero_da_conta: str,
    numero_da_conta_destino: str | None = None,
) -> dict:
    """Faz uma requisição de transação assíncrona."""
    corpo = {"tipo": tipo, "valor": valor, "numero_da_conta": numero_da_conta}
    if numero_da_conta_destino:
        corpo["numero_da_conta_destino"] = numero_da_conta_destino
    resposta = await client.post(
        "/api/transacao_bancaria",
        json=corpo,
        headers={"Authorization": f"Bearer {token}"},
    )
    return {
        "status_code": resposta.status_code,
        "body": resposta.json() if resposta.status_code < 500 else resposta.text,
    }


async def obter_saldo_async(
    client: httpx.AsyncClient, token: str, numero_da_conta: str
) -> Decimal:
    """Obtém o saldo de uma conta de forma assíncrona."""
    resposta = await client.get(
        f"/api/conta_bancarias?numero_da_conta={numero_da_conta}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resposta.status_code == 200 and resposta.json():
        return Decimal(resposta.json()[0]["saldo"])
    return Decimal("0.00")


async def criar_cliente_async(client: httpx.AsyncClient, token: str) -> dict:
    """Cria um cliente de teste via API assíncrona."""
    from contextos_de_negocios.utils.tipos_basicos import CPF

    dados = {"nome": "Cliente Async", "cpf": CPF.gerar()}
    resposta = await client.post(
        "/api/cliente", json=dados, headers={"Authorization": f"Bearer {token}"}
    )
    return resposta.json()


async def criar_conta_async(
    client: httpx.AsyncClient, token: str, cpf_cliente: str, saldo: str = "0.00"
) -> dict:
    """Cria uma conta bancária de teste via API assíncrona."""
    from random import randint

    dados = {
        "numero_da_conta": str(randint(100000, 999999)),
        "saldo": saldo,
        "cpf_cliente": cpf_cliente,
    }
    resposta = await client.post(
        "/api/conta_bancaria", json=dados, headers={"Authorization": f"Bearer {token}"}
    )
    return resposta.json()


@pytest.mark.asyncio
async def teste_concorrencia_asyncio_depositos(mock_usuario_api):
    """Teste de concorrência REAL com asyncio: N depósitos simultâneos.

    Usa asyncio.gather para executar requisições concorrentes e validar
    que o FOR UPDATE do PostgreSQL garante consistência.

    NOTA: Algumas transações podem falhar com erro de serialização (SerializationError)
    devido ao FOR UPDATE do PostgreSQL - isso é comportamento CORRETO que evita race conditions.
    O importante é que o saldo final seja consistente com as transações bem sucedidas.
    """
    db_module.ASYNC_ENGINE = None

    NUMERO_DEPOSITOS = 10
    VALOR_DEPOSITO = Decimal("10.00")
    SALDO_INICIAL = Decimal("0.00")
    token = mock_usuario_api.token

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        cliente = await criar_cliente_async(client, token)
        conta = await criar_conta_async(
            client, token, cliente["cpf"], str(SALDO_INICIAL)
        )
        numero_conta = conta["numero_da_conta"]

        tarefas = [
            fazer_transacao_async(
                client, token, "deposito", float(VALOR_DEPOSITO), numero_conta
            )
            for _ in range(NUMERO_DEPOSITOS)
        ]
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)

        # Contar sucessos (ignorar exceções de serialização)
        sucessos = sum(
            1 for r in resultados if isinstance(r, dict) and r["status_code"] == 200
        )
        saldo_final = await obter_saldo_async(client, token, numero_conta)

    saldo_esperado = SALDO_INICIAL + (VALOR_DEPOSITO * sucessos)

    # Resetar engine para próximos testes
    db_module.ASYNC_ENGINE = None

    # INVARIANTE: Saldo deve ser consistente com depósitos bem sucedidos
    assert saldo_final == saldo_esperado, (
        f"Saldo inconsistente! Final: {saldo_final}, Esperado: {saldo_esperado}. "
        f"Depósitos OK: {sucessos}/{NUMERO_DEPOSITOS}"
    )
    # Pelo menos alguns depósitos devem ter sucesso
    assert sucessos > 0, "Nenhum depósito teve sucesso"


@pytest.mark.asyncio
async def teste_concorrencia_asyncio_saques_race_condition(mock_usuario_api):
    """Teste de race condition REAL: múltiplos saques concorrentes com saldo justo.

    Este é o teste mais importante para validar que o FOR UPDATE do PostgreSQL
    evita race conditions. O PostgreSQL pode rejeitar algumas transações com
    SerializationError, mas NUNCA deve permitir saldo negativo.
    """
    db_module.ASYNC_ENGINE = None

    SALDO_INICIAL = Decimal("100.00")
    VALOR_SAQUE = Decimal("100.00")
    NUM_SAQUES = 5
    token = mock_usuario_api.token

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        cliente = await criar_cliente_async(client, token)
        conta = await criar_conta_async(
            client, token, cliente["cpf"], str(SALDO_INICIAL)
        )
        numero_conta = conta["numero_da_conta"]

        tarefas = [
            fazer_transacao_async(
                client, token, "saque", float(VALOR_SAQUE), numero_conta
            )
            for _ in range(NUM_SAQUES)
        ]
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)

        sucessos = sum(
            1 for r in resultados if isinstance(r, dict) and r["status_code"] == 200
        )
        saldo_final = await obter_saldo_async(client, token, numero_conta)

    # INVARIANTE CRÍTICO: Saldo NUNCA pode ser negativo
    assert saldo_final >= Decimal("0.00"), (
        f"RACE CONDITION! Saldo negativo: {saldo_final}"
    )

    # Com FOR UPDATE, no máximo 1 saque deve ter sucesso (saldo = 100, saque = 100)
    assert sucessos <= 1, (
        f"Mais saques que o permitido! Sucessos: {sucessos}, Saldo final: {saldo_final}"
    )

    # Saldo deve ser consistente
    saldo_esperado = SALDO_INICIAL - (VALOR_SAQUE * sucessos)

    # Resetar engine para próximos testes
    db_module.ASYNC_ENGINE = None

    assert saldo_final == saldo_esperado, (
        f"Saldo inconsistente: {saldo_final} != {saldo_esperado}"
    )


@pytest.mark.asyncio
async def teste_concorrencia_asyncio_transferencias_bidirecionais(mock_usuario_api):
    """Teste de deadlock: transferências A→B e B→A concorrentes.

    Este teste valida que a ordenação de locks (feita no __bloquear_e_obter_saldo)
    evita deadlocks em transferências bidirecionais.
    Algumas transferências podem falhar com SerializationError, mas a soma total
    DEVE ser conservada.
    """
    db_module.ASYNC_ENGINE = None

    SALDO_INICIAL = Decimal("100.00")
    NUM_TRANSFERENCIAS = 5
    VALOR_TRANSFERENCIA = Decimal("10.00")
    token = mock_usuario_api.token

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        cliente_a = await criar_cliente_async(client, token)
        cliente_b = await criar_cliente_async(client, token)
        conta_a = await criar_conta_async(
            client, token, cliente_a["cpf"], str(SALDO_INICIAL)
        )
        conta_b = await criar_conta_async(
            client, token, cliente_b["cpf"], str(SALDO_INICIAL)
        )
        numero_a = conta_a["numero_da_conta"]
        numero_b = conta_b["numero_da_conta"]

        tarefas_ab = [
            fazer_transacao_async(
                client,
                token,
                "transferencia",
                float(VALOR_TRANSFERENCIA),
                numero_a,
                numero_b,
            )
            for _ in range(NUM_TRANSFERENCIAS)
        ]
        tarefas_ba = [
            fazer_transacao_async(
                client,
                token,
                "transferencia",
                float(VALOR_TRANSFERENCIA),
                numero_b,
                numero_a,
            )
            for _ in range(NUM_TRANSFERENCIAS)
        ]

        await asyncio.gather(*tarefas_ab, *tarefas_ba, return_exceptions=True)

        saldo_a = await obter_saldo_async(client, token, numero_a)
        saldo_b = await obter_saldo_async(client, token, numero_b)

    # INVARIANTE CRÍTICO: Soma total DEVE ser conservada
    soma_total = saldo_a + saldo_b
    soma_esperada = SALDO_INICIAL * 2

    assert soma_total == soma_esperada, (
        f"ERRO: Soma não conservada! Total: {soma_total}, Esperado: {soma_esperada}. "
        f"Saldo A: {saldo_a}, Saldo B: {saldo_b}"
    )

    # Nenhum saldo negativo
    assert saldo_a >= Decimal("0.00"), f"Saldo A negativo: {saldo_a}"
    assert saldo_b >= Decimal("0.00"), f"Saldo B negativo: {saldo_b}"

    # Resetar engine para próximos testes
    db_module.ASYNC_ENGINE = None


@pytest.mark.asyncio
async def teste_concorrencia_asyncio_operacoes_mistas(mock_usuario_api):
    """Teste de stress: depósitos, saques e transferências concorrentes.

    Valida que a soma total é conservada mesmo com operações mistas concorrentes.
    """
    db_module.ASYNC_ENGINE = None

    SALDO_INICIAL = Decimal("1000.00")
    VALOR_DEPOSITO = Decimal("50.00")
    VALOR_SAQUE = Decimal("30.00")
    NUM_OPERACOES = 5
    token = mock_usuario_api.token

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        cliente1 = await criar_cliente_async(client, token)
        cliente2 = await criar_cliente_async(client, token)
        conta1 = await criar_conta_async(
            client, token, cliente1["cpf"], str(SALDO_INICIAL)
        )
        conta2 = await criar_conta_async(
            client, token, cliente2["cpf"], str(SALDO_INICIAL)
        )
        numero1 = conta1["numero_da_conta"]
        numero2 = conta2["numero_da_conta"]

        tarefas = []

        for _ in range(NUM_OPERACOES):
            tarefas.append(
                fazer_transacao_async(
                    client, token, "deposito", float(VALOR_DEPOSITO), numero1
                )
            )

        for _ in range(NUM_OPERACOES):
            tarefas.append(
                fazer_transacao_async(
                    client, token, "saque", float(VALOR_SAQUE), numero1
                )
            )

        for _ in range(NUM_OPERACOES):
            tarefas.append(
                fazer_transacao_async(
                    client, token, "transferencia", 20.00, numero1, numero2
                )
            )

        resultados = await asyncio.gather(*tarefas, return_exceptions=True)

        saldo1 = await obter_saldo_async(client, token, numero1)
        saldo2 = await obter_saldo_async(client, token, numero2)

    # Contar operações bem sucedidas (ignorar exceções)
    depositos_ok = saques_ok = transferencias_ok = 0
    for i, r in enumerate(resultados):
        if isinstance(r, dict) and r["status_code"] == 200:
            if i < NUM_OPERACOES:
                depositos_ok += 1
            elif i < NUM_OPERACOES * 2:
                saques_ok += 1
            else:
                transferencias_ok += 1

    # INVARIANTES
    assert saldo1 >= Decimal("0.00"), f"Saldo 1 negativo: {saldo1}"
    assert saldo2 >= Decimal("0.00"), f"Saldo 2 negativo: {saldo2}"

    # Soma total deve ser consistente (transferências não alteram soma)
    soma_total = saldo1 + saldo2
    soma_esperada = (
        SALDO_INICIAL * 2 + (VALOR_DEPOSITO * depositos_ok) - (VALOR_SAQUE * saques_ok)
    )

    assert soma_total == soma_esperada, (
        f"Soma inconsistente! Total: {soma_total}, Esperado: {soma_esperada}. "
        f"Depósitos: {depositos_ok}, Saques: {saques_ok}, Transferências: {transferencias_ok}"
    )

    # Resetar engine para próximos testes
    db_module.ASYNC_ENGINE = None
