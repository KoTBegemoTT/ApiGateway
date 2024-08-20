from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс настроек."""

    auth_host: str = 'host.docker.internal'
    auth_port: int = 8001

    transactions_host: str = 'host.docker.internal'
    transactions_port: int = 8002

    face_verification_host: str = 'host.docker.internal'
    face_verification_port: int = 8001

    @property
    def auth_service_url(self) -> str:
        """Ссылка на сервис аутентификации."""
        return f'http://{self.auth_host}:{self.auth_port}'

    @property
    def transactions_service_url(self) -> str:
        """Ссылка на сервис транзакции."""
        return f'http://{self.transactions_host}:{self.transactions_port}'

    @property
    def face_verification_service_url(self) -> str:
        """Ссылка на сервис верификации пользователя."""
        return f'http://{self.face_verification_host}:{self.face_verification_port}'  # noqa: E501


settings = Settings()
