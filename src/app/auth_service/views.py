from fastapi import HTTPException, Request, UploadFile, status
from opentracing import global_tracer

from app.auth_service.schemas import TokenSchema, UserSchema


async def register_view(user_in: UserSchema, request: Request) -> TokenSchema:
    """Регистрация пользователя."""
    with global_tracer().start_active_span('register_view') as scope:
        scope.span.set_tag('user_in', str(user_in))

        response = await request.state.auth_client.register(
            json=user_in.model_dump(),
        )

        if response.status_code == status.HTTP_201_CREATED:
            token = response.json()
            return TokenSchema(token=token)

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get('detail', 'No detail'),
        )


async def login_view(user_in: UserSchema, request: Request) -> TokenSchema:
    """Авторизация пользователя."""
    with global_tracer().start_active_span('login_view') as scope:
        scope.span.set_tag('user_in', str(user_in))

        response = await request.state.auth_client.login(
            json=user_in.model_dump(),
        )
        if response.status_code == status.HTTP_201_CREATED:
            token = response.json()
            return TokenSchema(token=token)

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get('detail', 'No detail'),
        )


async def check_token_dependency(user_id: int, request: Request) -> None:
    """Проверка токена. Возвращает имя пользователя."""
    with global_tracer().start_active_span('check_token_dependency') as scope:
        scope.span.set_tag('user_id', str(user_id))

        response = await request.state.auth_client.check_token(
            params={'user_id': user_id},
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get('detail', 'No detail'),
            )


async def verify_view(
    user_photo: UploadFile,
    user_id: int,
    request: Request,
) -> dict:
    """Подтверждение пользователя."""
    with global_tracer().start_active_span('verify_view') as scope:
        scope.span.set_tag('user_id', str(user_id))
        scope.span.set_tag('user_photo', str(user_photo))

        response = await request.state.auth_client.verify(
            files={'user_photo': await user_photo.read()},
            params={'user_id': user_id},
        )
        if response.status_code != status.HTTP_201_CREATED:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get('detail', 'No detail'),
            )

        return {'message': 'File saved successfully'}
