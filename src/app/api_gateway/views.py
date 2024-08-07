import asyncio

import httpx
from fastapi import HTTPException, status

from app.settings import settings


async def ready_check_view() -> None:
    """Проверка состояния сервисов auth_service и transactions_service."""
    async with httpx.AsyncClient() as client:
        requests = [
            client.get(url=f'{settings.auth_service_url}/healthz/ready/'),
            client.get(
                url=f'{settings.transactions_service_url}/healthz/ready/',
            ),
        ]

        for first_completed in asyncio.as_completed(requests):
            try:
                response = await first_completed
            except httpx.ReadTimeout:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
