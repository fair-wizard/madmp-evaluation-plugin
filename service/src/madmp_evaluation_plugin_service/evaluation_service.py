import httpx


class EvaluationServiceClient:

    def __init__(self, api_url: str, client: httpx.AsyncClient) -> None:
        self.api_url = api_url.rstrip('/')
        self.client = client
        self.client.base_url = httpx.URL(self.api_url)
        self.client.headers.update({
            'User-Agent': 'maDMP-Evaluation-Service-Client/0.1.0',
        })

    async def get_benchmarks(self) -> list[dict]:
        response = await self.client.get(
            url='/benchmarks/list',
        )
        response.raise_for_status()
        return response.json()

    async def get_tests(self) -> list[dict]:
        response = await self.client.get(
            url='/tests/info',
        )
        response.raise_for_status()
        return response.json()

    async def evaluate_benchmark(self, benchmark: str, madmp: str) -> list[dict]:
        response = await self.client.post(
            url='/assess/benchmark',
            data={
                'benchmark': benchmark,
            },
            files={
                'maDMP': ('madmp.json', madmp.encode('utf-8'), 'application/json'),
            },
        )
        response.raise_for_status()
        return response.json()

    async def evaluate_test(self, test: str, madmp: str) -> dict:
        response = await self.client.post(
            url='/assess/test',
            data={
                'test': test,
            },
            files={
                'maDMP': ('madmp.json', madmp.encode('utf-8'), 'application/json'),
            },
        )
        response.raise_for_status()
        return response.json()
