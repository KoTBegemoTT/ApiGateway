import httpx
from opentracing import Format, global_tracer


class ServiceClient:
    """Класс для работы с HTTP-клиентами."""

    def __init__(self, session: httpx.AsyncClient, base_url: str):
        self.session = session
        self.base_url = base_url

    async def request(self, method: str, path: str, **kwargs):
        """Метод для отправки запросов."""
        url = f'{self.base_url}{path}'
        headers = kwargs.get('headers', {})

        span = global_tracer().active_span
        if span:
            global_tracer().inject(span.context, Format.HTTP_HEADERS, headers)

        kwargs['headers'] = headers

        return await self.session.request(method, url, **kwargs)
