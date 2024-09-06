from fastapi import APIRouter, Request, status

from app.auth_service.views import check_token_dependency
from app.transaction_service.schemas import (
    CreateTransactionSchema,
    TransactionOutSchema,
    TransactionReportSchema,
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
async def create_transaction(
    transaction: CreateTransactionSchema,
    request: Request,
) -> None:
    """Создание новой транзакции."""
    await check_token_dependency(transaction.user_id, request)
    await create_transaction_view(transaction, request)


@router.post(
    '/report/',
    status_code=status.HTTP_201_CREATED,
)
async def get_transactions(
    transaction_report: TransactionReportSchema,
    request: Request,
) -> list[TransactionOutSchema]:
    """Получение списка транзакции."""
    await check_token_dependency(transaction_report.user_id, request)
    return await get_transactions_view(transaction_report, request)
