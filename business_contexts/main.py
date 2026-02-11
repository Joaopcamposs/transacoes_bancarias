from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from business_contexts.utils.constants import SENTRY_DSN
from infra import start_mappers
from infra.database import (
    create_first_user,
    get_async_engine,
    mapper_registry,
)

from business_contexts.entrypoints.public_api.security_resources import (
    router as security_router,
)
from business_contexts.entrypoints.public_api.bank_account_resources import (
    router as bank_account_router,
)
from business_contexts.entrypoints.public_api.bank_transaction_resources import (
    router as bank_transaction_router,
)
from business_contexts.entrypoints.public_api.client_resources import (
    router as client_router,
)
from business_contexts.entrypoints.public_api.user_resources import (
    router as user_router,
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Gerencia o ciclo de vida da aplicação, inicializando mapeadores e banco de dados."""
    start_mappers()
    async with get_async_engine().begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    await create_first_user()
    yield


app: FastAPI = FastAPI(
    title="API Transações Bancárias",
    description="APIs REST",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)


@app.get("/")
async def root() -> dict[str, str]:
    """Rota raiz da aplicação."""
    return {"message": "Hello World"}


@app.get("/test")
async def test() -> set[str]:
    """Rota de teste para verificar se a aplicação está funcionando."""
    return {"OK"}


@app.get("/sentry-debug")
async def trigger_error() -> float:
    """Rota para testar a integração com o Sentry."""
    return 1 / 0


# CORS
origins: list[str] = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# include routes from api
app.include_router(security_router)
app.include_router(bank_account_router)
app.include_router(bank_transaction_router)
app.include_router(client_router)
app.include_router(user_router)
