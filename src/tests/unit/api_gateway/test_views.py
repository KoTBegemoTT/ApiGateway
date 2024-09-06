import httpx
import pytest
from fastapi import HTTPException, status

from app.api_gateway.views import ready_check_view
from app.settings import settings


@pytest.mark.asyncio
async def test_ready_check(monkeypatch):
    async def get_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status.HTTP_200_OK)

    monkeypatch.setattr(
        'app.api_gateway.views.httpx.AsyncClient.get',
        get_mock,
    )

    await ready_check_view()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'auth_status, transactions_status',
    [
        pytest.param(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            status.HTTP_200_OK,
            id='auth_error',
        ),
        pytest.param(
            status.HTTP_200_OK,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            id='transaction_error',
        ),
        pytest.param(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            id='all_error',
        ),
    ],
)
async def test_ready_check_fail(monkeypatch, auth_status, transactions_status):
    async def get_mock(self, url, *args, **kwargs) -> httpx.Response:
        if url == f'{settings.auth_service_url}/api/healthz/ready/':
            return httpx.Response(auth_status)
        elif url == f'{settings.transactions_service_url}/api/healthz/ready/':
            return httpx.Response(transactions_status)

        raise ValueError('Wrong url')

    monkeypatch.setattr(
        'app.api_gateway.views.httpx.AsyncClient.get',
        get_mock,
    )

    with pytest.raises(HTTPException) as excinfo:
        await ready_check_view()

    assert excinfo.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
