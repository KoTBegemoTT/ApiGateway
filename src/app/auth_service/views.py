import httpx
from fastapi import HTTPException, status

from app.auth_service.schemas import TokenSchema, UserSchema
from app.settings import settings


async def register_view(user_in: UserSchema) -> TokenSchema:
    """Регистрация пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{settings.auth_service_url}/register/',
            json=user_in.model_dump(),
        )

    if response.status_code == status.HTTP_201_CREATED:
        token = response.json()
        return TokenSchema(token=token)

    raise HTTPException(
        status_code=response.status_code,
        detail=response.json().get('detail', 'No detail'),
    )


async def login_view(user_in: UserSchema) -> TokenSchema:
    """Авторизация пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{settings.auth_service_url}/auth/',
            json=user_in.model_dump(),
        )
    if response.status_code == status.HTTP_201_CREATED:
        token = response.json()
        return TokenSchema(token=token)

    raise HTTPException(
        status_code=response.status_code,
        detail=response.json().get('detail', 'No detail'),
    )


async def check_token_dependency(user_id: int) -> None:
    """Проверка токена. Возвращает имя пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{settings.auth_service_url}/check_token/',
            params={'user_id': user_id},
        )
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get('detail', 'No detail'),
        )
