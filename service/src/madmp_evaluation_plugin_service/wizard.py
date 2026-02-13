import httpx


class WizardClient:

    def __init__(self, api_url: str, client: httpx.AsyncClient):
        self.api_url = api_url.rstrip('/')
        self.client = client
        self.client.base_url = httpx.URL(self.api_url)
        self.client.headers.update({
            'User-Agent': 'maDMP-Wizard-Client/0.1.0',
        })

    async def get_project(self, project_uuid: str, user_token: str) -> dict:
        response = await self.client.get(
            url=f'/projects/{project_uuid}/questionnaire',
            headers={
                'Authorization': f'Bearer {user_token}',
            }
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def to_madmp(project_data: dict) -> dict:
        # TODO: map project data to maDMP format
        return {"dmp": {}}
