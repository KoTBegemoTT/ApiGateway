from fastapi import APIRouter, status

from app.auth_service.schemas import TokenSchema, UserSchema
from app.auth_service.views import check_token_view, login_view, register_view

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
async def check_token(token: str) -> str:
    """Проверка токена. Возвращает имя пользователя."""
    return await check_token_view(token)
