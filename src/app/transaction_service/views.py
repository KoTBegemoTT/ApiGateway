from fastapi import Request
from opentracing import global_tracer

from app.transaction_service.schemas import (
    CreateTransactionSchema,
    TransactionOutSchema,
    TransactionReportSchema,
)


async def create_transaction_view(
    transaction: CreateTransactionSchema,
    request: Request,
) -> None:
    """Создание новой транзакции."""
    with global_tracer().start_active_span('create_transaction_view') as scope:
        scope.span.set_tag('transaction', str(transaction))

        await request.state.transaction_client.create_transaction(
            json=transaction.model_dump(),
        )


async def get_transactions_view(
    report: TransactionReportSchema,
    request: Request,
) -> list[TransactionOutSchema]:
    """Получение списка транзакций."""
    with global_tracer().start_active_span('get_transactions_view') as scope:
        scope.span.set_tag('report', str(report))

        response = await request.state.transaction_client.get_transactions(
            json=report.model_dump(),
        )

        transactions = [
            TransactionOutSchema.model_validate(transaction)
            for transaction in response.json()
        ]
        return transactions  # noqa: WPS331
