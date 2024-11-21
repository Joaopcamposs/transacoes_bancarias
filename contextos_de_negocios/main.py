import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from contextos_de_negocios.utils.constantes import SENTRY_DSN
from infra.banco_de_dados import criar_primeiro_usuario, get_engine, Base

from contextos_de_negocios.pontos_de_entrada.api_publica.recursos_seguranca import (
    router as servicos_router,
)
from contextos_de_negocios.pontos_de_entrada.api_publica.recursos_conta_bancaria import (
    router as conta_bancaria_router,
)
from contextos_de_negocios.pontos_de_entrada.api_publica.recursos_transacao_bancaria import (
    router as transacao_bancaria_router,
)
from contextos_de_negocios.pontos_de_entrada.api_publica.recursos_cliente import (
    router as cliente_router,
)
from contextos_de_negocios.pontos_de_entrada.api_publica.recursos_usuario import (
    router as usuario_router,
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_tracing=True,
)

app = FastAPI(
    title="API Transações Bancárias",
    description="APIs REST",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test")
async def test():
    return {"OK"}


@app.get("/sentry-debug")
async def trigger_error():
    # apenas para testar o sentry
    return 1 / 0


@app.on_event("startup")
async def startup():
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await criar_primeiro_usuario()


# CORS
origins: list = [
    "http://localhost",
    "http://18.117.123.228",
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
app.include_router(servicos_router)
app.include_router(conta_bancaria_router)
app.include_router(transacao_bancaria_router)
app.include_router(cliente_router)
app.include_router(usuario_router)
