from fastapi import APIRouter, UploadFile, status

from app.auth_service.schemas import TokenSchema, UserSchema
from app.auth_service.views import (
    check_token_dependency,
    login_view,
    register_view,
    verify_view,
)

router = APIRouter(tags=['auth_service'])


@router.post(
    '/register/',
    response_model=TokenSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_in: UserSchema) -> TokenSchema:
    """Регистрация пользователя."""
    return await register_view(user_in)


@router.post(
    '/auth/',
    response_model=TokenSchema,
    status_code=status.HTTP_201_CREATED,
)
async def login(user_in: UserSchema) -> TokenSchema:
    """Авторизация пользователя."""
    return await login_view(user_in)


@router.get(
    '/check_token/',
    status_code=status.HTTP_200_OK,
)
async def check_token(user_id: int) -> None:
    """Проверка токена. Возвращает имя пользователя."""
    await check_token_dependency(user_id)


@router.post(
    '/verify/',
    status_code=status.HTTP_201_CREATED,
)
async def verify(user_photo: UploadFile, user_id: int) -> dict:
    """Подтверждение пользователя."""
    await check_token_dependency(user_id)
    return await verify_view(user_photo, user_id)
