import httpx
from opentracing import global_tracer

from app.settings import settings


async def image_to_vector(path: str) -> list[float]:
    """Функция превращает изображение в вектор."""
    with global_tracer().start_active_span('image_to_vector') as scope:
        scope.span.set_tag('path', str(path))

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{settings.face_verification_service_url}/get_vector/',
                params={'path': path},
            )
        return response.json()
