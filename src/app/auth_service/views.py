import httpx
from fastapi import HTTPException, status

from app.auth_service.schemas import TokenSchema, UserSchema
from app.settings import settings


async def register_view(user_in: UserSchema) -> TokenSchema:
    """Регистрация пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{settings.auth_service_url}/register',
            json=user_in.model_dump(),
        )
    token = response.json().get('token')
    return TokenSchema(token=token)


async def login_view(user_in: UserSchema) -> TokenSchema:
    """Авторизация пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{settings.auth_service_url}/auth',
            json=user_in.model_dump(),
        )
    token = response.json().get('token')

    if token:
        return TokenSchema(token=token)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Incorrect username or password',
    )
