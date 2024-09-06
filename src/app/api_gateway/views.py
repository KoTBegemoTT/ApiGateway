import asyncio

import httpx
from fastapi import HTTPException, status
from opentracing import global_tracer

from app.settings import settings


async def ready_check_view() -> None:
    """Проверка состояния сервисов auth_service и transactions_service."""
    with global_tracer().start_active_span('ready_check_view') as scope:
        async with httpx.AsyncClient() as client:
            requests = [
                client.get(
                    url=f'{settings.auth_service_url}/api/healthz/ready/',
                ),
                client.get(
                    url=f'{settings.transactions_service_url}/api/healthz/ready/',  # noqa: E501
                ),
            ]

            scope.span.set_tag('requests', str(requests))

            for first_completed in asyncio.as_completed(requests):
                try:
                    response = await first_completed
                    scope.span.set_tag('response', str(response))
                except httpx.ReadTimeout:
                    scope.span.set_tag('error', 'timeout')
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )

                if response.status_code != status.HTTP_200_OK:
                    scope.span.set_tag('error', 'service_unavailable')
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )
