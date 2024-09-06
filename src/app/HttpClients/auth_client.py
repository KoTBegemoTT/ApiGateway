from app.HttpClients.base_client import ServiceClient


class AuthServiceClient(ServiceClient):
    """Клиент для работы с сервисом аутентификации."""

    async def register(self, json):
        """Регистрация пользователя."""
        return await self.request('POST', '/api/register/', json=json)

    async def login(self, json):
        """Авторизация пользователя."""
        return await self.request('POST', '/api/auth/', json=json)

    async def check_token(self, params):
        """Проверка токена. Возвращает имя пользователя."""
        return await self.request('GET', '/api/check_token/', params=params)

    async def verify(self, files, params):
        """Подтверждение пользователя."""
        return await self.request(
            'POST',
            '/api/verify/',
            files=files,
            params=params,
        )
