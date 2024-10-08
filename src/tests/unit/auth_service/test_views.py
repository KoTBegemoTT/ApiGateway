from unittest.mock import Mock

import httpx
import pytest
from fastapi import HTTPException, status

from app.auth_service.schemas import UserSchema
from app.auth_service.views import (
    check_token_dependency,
    login_view,
    register_view,
    verify_view,
)


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
        return httpx.Response(status.HTTP_201_CREATED, json=token)

    request = Mock()
    request.state.auth_client.register = post_mock

    response_schema = await register_view(
        UserSchema(name=username, password=password),
        request,
    )

    assert response_schema.token == token


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'username, password, status, detail',
    [
        pytest.param('exist_user', 'passowrd', status.HTTP_409_CONFLICT,
                     'Username already exists', id='user_exists'),
    ],
)
async def test_register_view_fail(
    monkeypatch, username, password, status, detail,
):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status_code=status, json={'detail': detail})

    request = Mock()
    request.state.auth_client.register = post_mock

    with pytest.raises(HTTPException) as excinfo:
        await register_view(
            UserSchema(name=username, password=password),
            request,
        )

    assert excinfo.value.status_code == status
    assert excinfo.value.detail == detail


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
        return httpx.Response(status.HTTP_201_CREATED, json=token)

    request = Mock()
    request.state.auth_client.login = post_mock

    response_schema = await login_view(
        UserSchema(name=username, password=password),
        request,
    )

    assert response_schema.token == token


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'username, password, status, detail',
    [
        pytest.param('wrong_user', 'wrong_password', status.HTTP_403_FORBIDDEN,
                     'Incorrect username or password', id='forbidden'),
    ],
)
async def test_login_view_fail(
    monkeypatch, username, password, status, detail,
):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status_code=status, json={'detail': detail})

    request = Mock()
    request.state.auth_client.login = post_mock

    with pytest.raises(HTTPException) as excinfo:
        await login_view(UserSchema(name=username, password=password), request)

    assert excinfo.value.status_code == status
    assert excinfo.value.detail == detail


@pytest.mark.asyncio
async def test_check_token_dependency(monkeypatch):
    async def get_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status.HTTP_200_OK, json='admin')

    request = Mock()
    request.state.auth_client.check_token = get_mock

    await check_token_dependency(user_id=0, request=request)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'status, detail',
    [
        pytest.param(status.HTTP_401_UNAUTHORIZED, 'token expired',
                     id='token_expired'),
        pytest.param(status.HTTP_401_UNAUTHORIZED, 'invalid token',
                     id='invalid_token'),
        pytest.param(status.HTTP_404_NOT_FOUND, 'token not found',
                     id='token_not_found'),
    ],
)
async def test_check_token_dependency_fail(monkeypatch, status, detail):
    async def get_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status_code=status, json={'detail': detail})

    request = Mock()
    request.state.auth_client.check_token = get_mock

    with pytest.raises(HTTPException) as excinfo:
        await check_token_dependency(user_id=0, request=request)

    assert excinfo.value.status_code == status
    assert excinfo.value.detail == detail


@pytest.mark.asyncio
async def test_verify_view(monkeypatch):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status.HTTP_201_CREATED)

    request = Mock()
    request.state.auth_client.verify = post_mock

    async def read_mock(*args, **kwargs) -> bytes:
        return b'file'

    upload_file_mock = Mock(read=read_mock)

    result = await verify_view(upload_file_mock, 1, request)

    assert result['message'] == 'File saved successfully'


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'status, detail',
    [
        pytest.param(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'unprocessable',
            id='unprocessable',
        ),
        pytest.param(
            status.HTTP_400_BAD_REQUEST,
            'bad request',
            id='bad_request',
        ),
    ],
)
async def test_verify_view_fail(monkeypatch, status, detail):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status, json={'detail': detail})

    request = Mock()
    request.state.auth_client.verify = post_mock

    async def read_mock(*args, **kwargs) -> bytes:
        return b'file'

    upload_file_mock = Mock(read=read_mock)

    # action
    with pytest.raises(HTTPException) as excinfo:
        await verify_view(upload_file_mock, 1, request)

    # assert
    assert excinfo.value.status_code == status
    assert excinfo.value.detail == detail
