# Implementation Plan - Consistency and Concurrency Improvements

## Problem Description
The current banking transaction simulator has a race condition in the [cadastrar_transacao_bancaria](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/servicos/executores/transacao_bancaria.py#18-41) service. The service reads the account balance in one database session, performs a check in memory, and then writes the transaction in a separate database session. This "Check-Then-Act" pattern is not atomic, allowing potential overdrafts under concurrent load despite the use of explicit locking in the write phase.

## User Review Required
> [!IMPORTANT]
> This change introduces a Unit of Work (UoW) pattern to manage database sessions. This is a structural change to how services interact with repositories.

## Proposed Changes

### Infrastructure Layer
#### [NEW] [unit_of_work.py](file:///Users/joaopcamposs/Dev/transacoes_bancarias/libs/ddd/adaptadores/unit_of_work.py)
- Create a `AbstractUnitOfWork` and `SqlAlchemyUnitOfWork` class.
- The UoW will manage the `AsyncSession` and provide access to repositories ([ContaBancariaRepoDominio](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/conta_bancaria.py#12-130), [TransacaoBancariaRepoDominio](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/transacao_bancaria.py#13-88), etc.).
- It will handle [commit](file:///Users/joaopcamposs/Dev/transacoes_bancarias/libs/ddd/adaptadores/repositorio.py#16-18) and [rollback](file:///Users/joaopcamposs/Dev/transacoes_bancarias/libs/ddd/adaptadores/repositorio.py#23-26) atomically.

#### [MODIFY] [repositorio.py](file:///Users/joaopcamposs/Dev/transacoes_bancarias/libs/ddd/adaptadores/repositorio.py)
- Update [BaseRepoPadrao](file:///Users/joaopcamposs/Dev/transacoes_bancarias/libs/ddd/adaptadores/repositorio.py#28-45) (and subclasses) to accept an optional existing session in [__init__](file:///Users/joaopcamposs/Dev/transacoes_bancarias/libs/ddd/adaptadores/repositorio.py#29-31).
- If a session is provided, use it; otherwise, create a new one (backward compatibility).

### Business Context - Repositories
#### [MODIFY] [conta_bancaria.py](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/conta_bancaria.py)
- Ensure it works with the session passed from UoW.
- Add/Expose a method [bloquear_conta(id)](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/transacao_bancaria.py#71-88) or ensure [consultar_por_numero_da_conta](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/conta_bancaria.py#49-84) can optionally lock. *Correction*: Better to have a specific method or use `with_for_update` in the query within the service/UoW flow. I will add a `consultar_por_numero_da_conta_com_lock` or similar, or just rely on the service to call a lock method.
- Actually, [TransacaoBancariaRepoDominio](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/transacao_bancaria.py#13-88) already has [__bloquear_contas_para_concorrencia](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/transacao_bancaria.py#71-88). I should move this logic or make it accessible via [ContaBancariaRepoDominio](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/conta_bancaria.py#12-130) or simply use it within the UoW context.

#### [MODIFY] [transacao_bancaria.py](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/repositorio/repo_dominio/transacao_bancaria.py)
- Remove the internal session management and explicit locking *if* it's handled by the service/UoW (or keep it but ensure it uses the UoW session).
- Remove the implicit balance update if we move that logic to the service (optional, but cleaner). For now, to minimize changes, I will keep the update logic but ensure it runs in the same session as the check.

### Business Context - Services
#### [MODIFY] [transacao_bancaria.py](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/servicos/executores/transacao_bancaria.py)
- Refactor [cadastrar_transacao_bancaria](file:///Users/joaopcamposs/Dev/transacoes_bancarias/contextos_de_negocios/servicos/executores/transacao_bancaria.py#18-41) to use `SqlAlchemyUnitOfWork`.
- Flow:
    1.  `async with uow:`
    2.  `uow.contas.bloquear_por_numero(numero_conta)` (New method to ensure lock before read)
    3.  `conta = await uow.contas.consultar_por_numero_da_conta(...)`
    4.  `conta.nova_transacao(...)` (Domain check)
    5.  `await uow.transacoes.adicionar(...)`
    6.  `await uow.commit()`

## Verification Plan

### Automated Tests
- Run existing concurrency tests: `pytest testes/test_api_transacoes_e_concorrencia.py`
- These tests simulate concurrent requests and verify final balances. They should pass (and potentially be more stable/correct) with the fix.

### Manual Verification
- I will create a script to simulate a high volume of concurrent transactions to verify consistency if the existing tests are insufficient.
