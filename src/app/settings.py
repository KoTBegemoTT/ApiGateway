from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс настроек."""

    # Общие настройки
    service_name: str = 'gateway-service'

    # Настройки сервиса аутентификации
    auth_host: str = 'host.docker.internal'
    auth_port: str = '8001'

    # Настройки сервиса транзакции
    transactions_host: str = 'host.docker.internal'
    transactions_port: str = '8002'

    # Настройки сервиса верификации
    face_verification_host: str = 'host.docker.internal'
    face_verification_port: str = '8003'

    # Настройки Jaeger
    jaeger_agent_host: str = 'host.docker.internal'
    jaeger_agent_port: str = '6831'
    jaeger_sampler_type: str = 'probabilistic'
    jaeger_sampler_param: float = 1.0
    jaeger_logging: bool = True
    jaeger_validate: bool = True

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
