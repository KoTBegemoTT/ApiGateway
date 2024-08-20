from datetime import datetime

import httpx
import pytest

from app.transaction_service import views  # noqa: F401
from app.transaction_service.schemas import (
    CreateTransactionSchema,
    TransactionReportSchema,
    TransactionType,
)
from app.transaction_service.views import (
    create_transaction_view,
    get_transactions_view,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'transaction',
    [
        pytest.param(
            CreateTransactionSchema(
                user_id=1,
                amount=100,
                transaction_type=TransactionType.DEPOSIT,
            ),
            id='user_1',
        ),
    ],
)
async def test_create_transaction_view_no_error(monkeypatch, transaction):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(201)

    monkeypatch.setattr(
        'app.transaction_service.views.httpx.AsyncClient.post',
        post_mock,
    )

    await create_transaction_view(transaction)


@pytest.mark.asyncio
async def test_get_transactions_view(monkeypatch):
    async def post_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(
            201,
            json=[
                {
                    'user_id': 1,
                    'amount': 100,
                    'transaction_type_id': 1,
                    'date': '2024-01-01',
                },
            ],
        )

    monkeypatch.setattr(
        'app.transaction_service.views.httpx.AsyncClient.post',
        post_mock,
    )

    transacitons = await get_transactions_view(
        TransactionReportSchema
        (
            user_id=1,
            date_start=datetime(2024, 1, 1),
            date_end=datetime(2124, 1, 1),
        ),
    )

    assert len(transacitons) == 1
    assert transacitons[0].amount == 100
    assert transacitons[0].transaction_type_id
    assert transacitons[0].date == datetime(2024, 1, 1)
