import uvicorn
from fastapi import FastAPI

from app.api_gateway.urls import router as api_gateway_router
from app.auth_service.urls import router as auth_router
from app.face_verification_service.urls import (
    router as face_verification_router,
)
from app.transaction_service.urls import router as transaction_router

app = FastAPI()
app.include_router(auth_router, prefix='/auth-service')
app.include_router(transaction_router, prefix='/transaction-service')
app.include_router(
    face_verification_router, prefix='/face-verification-service',
)
app.include_router(api_gateway_router, prefix='/api-gateway')


@app.get('/')
async def root():
    """Стартовая страница."""
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True,
        host='0.0.0.0',  # noqa: S104
        port=8000,  # noqa: WPS432
    )
