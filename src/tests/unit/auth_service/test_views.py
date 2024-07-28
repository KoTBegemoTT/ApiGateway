import httpx
import pytest
from fastapi import HTTPException

from app.auth_service import views  # noqa: F401
from app.auth_service.schemas import UserSchema
from app.auth_service.views import login_view, register_view


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'username, password, token',
    [
        pytest.param('user_1', 'password', 'token', id='user_1'),
        pytest.param('user', 'user', 'user', id='user'),
    ],
)
async def test_register_view(monkeypatch, username, password, token):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(200, json={'token': token})

    monkeypatch.setattr(
        'app.auth_service.views.httpx.AsyncClient.post',
        post_mock,
    )

    response_schema = await register_view(
        UserSchema(name=username, password=password))

    assert response_schema.token == token


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'username, password, token',
    [
        pytest.param('user_1', 'password', 'token', id='user_1'),
        pytest.param('user', 'user', 'user', id='user'),
    ],
)
async def test_login_view(monkeypatch, username, password, token):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(200, json={'token': token})

    monkeypatch.setattr(
        'app.auth_service.views.httpx.AsyncClient.post',
        post_mock,
    )

    response_schema = await login_view(
        UserSchema(name=username, password=password))

    assert response_schema.token == token


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'username, password, token',
    [
        pytest.param('no_user', 'no_password', None, id='user_not_found'),
    ],
)
async def test_login_view_fail(monkeypatch, username, password, token):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(200, json={'token': token})

    monkeypatch.setattr(
        'app.auth_service.views.httpx.AsyncClient.post',
        post_mock,
    )

    with pytest.raises(HTTPException) as excinfo:
        await login_view(UserSchema(name=username, password=password))

    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == 'Incorrect username or password'
