import httpx

from app.settings import settings


async def image_to_vector(path: str) -> list[float]:
    """Функция превращает изображение в вектор."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{settings.face_verification_service_url}/get_vector/',
            params={'path': path},
        )
    return response.json()
