import httpx
import pytest

from app.face_verification_service import views  # noqa: F401
from app.face_verification_service.views import image_to_vector


@pytest.mark.asyncio
async def test_image_to_vector(monkeypatch):
    async def get_mock(*args, **kwargs) -> httpx.Response:
        return httpx.Response(200, json=[1, 2, 3])

    monkeypatch.setattr(
        'app.face_verification_service.views.httpx.AsyncClient.get',
        get_mock,
    )

    vector = await image_to_vector('path/to/image.jpg')

    assert vector == [1, 2, 3]
