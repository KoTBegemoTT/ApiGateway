class Settings():
    """Класс настроек."""

    auth_service_url: str = 'http://host.docker.internal:8001'
    transactions_service_url: str = 'http://host.docker.internal:8002/transactions'  # noqa: E501
    face_verification_service_url: str = 'http://host.docker.internal:8003'


settings = Settings()
