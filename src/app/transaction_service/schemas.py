from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_serializer


class TransactionType(Enum):
    """Тип транзакции."""

    DEPOSIT = 'Пополнение'
    WITHDRAWAL = 'Снятие'


class CreateTransactionSchema(BaseModel):
    """Схема создания транзакции."""

    user_id: int
    amount: int
    transaction_type: TransactionType

    @field_serializer('transaction_type')
    def serialize_transaction_type(self, transaction_type: TransactionType):
        """Функция сериализации типа транзакции."""
        return transaction_type.value


class TransactionSchema(BaseModel):
    """Схема создания транзакции."""

    amount: int
    transaction_type: TransactionType
    date: datetime


class TransactionOutSchema(BaseModel):
    """Схема вывода транзакции."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    amount: int
    transaction_type_id: int
    date: datetime


class TransactionReportSchema(BaseModel):
    """Схема отчета о транзакциях."""

    user_id: int
    date_start: datetime
    date_end: datetime

    @field_serializer('date_start', 'date_end')
    def serialize_date(self, date: datetime):
        """Функция сериализации даты."""
        return date.isoformat()
