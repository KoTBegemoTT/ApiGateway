from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.api_gateway.urls import router as api_gateway_router
from app.auth_service.urls import router as auth_router
from app.external.jaeger import initialize_jaeger_tracer
from app.face_verification_service.urls import (
    router as face_verification_router,
)
from app.HttpClients.auth_client import AuthServiceClient
from app.HttpClients.transaction_client import TransactionServiceClient
from app.middleware import tracing_middleware
from app.settings import settings
from app.transaction_service.urls import router as transaction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Настройка при запуске и остановке приложения."""
    session = httpx.AsyncClient()
    initialize_jaeger_tracer()
    yield {
        'auth_client': AuthServiceClient(session, settings.auth_service_url),
        'transaction_client': TransactionServiceClient(
            session,
            settings.transactions_service_url,
        ),
    }


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/api/auth-service')
app.include_router(transaction_router, prefix='/api/transaction-service')
app.include_router(
    face_verification_router, prefix='/api/face-verification-service',
)
app.include_router(api_gateway_router, prefix='/api/api-gateway')

app.add_middleware(BaseHTTPMiddleware, dispatch=tracing_middleware)


@app.get('/')
async def root():
    """Стартовая страница."""
    return {'message': 'Hello World'}


@app.get('/ready', status_code=status.HTTP_200_OK)
async def ready_check():
    """Проверка состояния сервиса."""
    return {'message': 'Service is ready'}


@app.get('/live', status_code=status.HTTP_200_OK)
async def live_check():
    """Проверка состояния сервиса."""
    return {'message': 'Service is live'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True,
        host='0.0.0.0',  # noqa: S104
        port=8000,  # noqa: WPS432
    )
