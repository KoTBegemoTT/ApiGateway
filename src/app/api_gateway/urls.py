from fastapi import APIRouter, status

from app.api_gateway.views import ready_check_view

router = APIRouter(tags=['api_gateway'])


@router.get(
    '/healthz/ready/',
    status_code=status.HTTP_200_OK,
)
async def ready_check() -> None:
    """Проверка состояния сервиса."""
    await ready_check_view()
