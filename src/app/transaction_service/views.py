import httpx

from app.settings import settings
from app.transaction_service.schemas import (
    CreateTransactionSchema,
    TransactionReportSchema,
    TransactionSchema,
)


async def create_transaction_view(
    transaction: CreateTransactionSchema,
) -> None:
    """Создание новой транзакции."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f'{settings.transactions_service_url}/create/',
            json=transaction.model_dump(),
        )


async def get_transactions_view(
    report: TransactionReportSchema,
) -> list[TransactionSchema]:
    """Получение списка транзакций."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{settings.transactions_service_url}/report/',
            json=report.model_dump(),
        )

    transactions = [
        TransactionSchema(**transaction) for transaction in response.json()
    ]
    return transactions  # noqa: WPS331
