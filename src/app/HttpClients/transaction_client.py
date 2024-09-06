from app.HttpClients.base_client import ServiceClient


class TransactionServiceClient(ServiceClient):
    """Клиент для работы с сервисом транзакции."""

    async def create_transaction(self, json):
        """Создание новой транзакции."""
        return await self.request(
            'POST',
            '/api/transactions/create/',
            json=json,
        )

    async def get_transactions(self, json):
        """Получение списка транзакций."""
        return await self.request(
            'POST',
            '/api/transactions/report/',
            json=json,
        )
