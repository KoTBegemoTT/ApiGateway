from fastapi import APIRouter, status

from app.auth_service.views import check_token_dependency
from app.transaction_service.schemas import (
    CreateTransactionSchema,
    TransactionReportSchema,
    TransactionSchema,
)
from app.transaction_service.views import (
    create_transaction_view,
    get_transactions_view,
)

router = APIRouter(tags=['transaction_service'])


@router.post(
    '/create/',
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(transaction: CreateTransactionSchema) -> None:
    """Создание новой транзакции."""
    await check_token_dependency(transaction.user_id)
    await create_transaction_view(transaction)


@router.post(
    '/report/',
    status_code=status.HTTP_201_CREATED,
)
async def get_transactions(
    transaction_report: TransactionReportSchema,
) -> list[TransactionSchema]:
    """Получение списка транзакции."""
    await check_token_dependency(transaction_report.user_id)
    return await get_transactions_view(transaction_report)
