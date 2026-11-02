import datetime

import httpx

from . import mapping


def _to_datetime_str(value: str) -> str:
    timestamp = datetime.datetime.fromisoformat(value)
    return timestamp.astimezone(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


class WizardClient:

    def __init__(self, api_url: str, client: httpx.AsyncClient) -> None:
        self.api_url = api_url.rstrip('/')
        self.client = client
        self.client.base_url = httpx.URL(self.api_url)
        self.client.headers.update({
            'User-Agent': 'maDMP-Wizard-Client/0.1.0',
        })

    @property
    def default_client_url(self) -> str:
        return self.api_url.removesuffix('/wizard-api').removesuffix('/api').removesuffix('-api')

    async def get_project(self, project_uuid: str, user_token: str) -> dict:
        response = await self.client.get(
            url=f'/projects/{project_uuid}/questionnaire',
            headers={
                'Authorization': f'Bearer {user_token}',
            },
        )
        response.raise_for_status()
        return response.json()

    async def _get_project_event_time(self, project_uuid: str, user_token: str, order: str) -> str | None:
        response = await self.client.get(
            url=f'/projects/{project_uuid}/events',
            params={'size': 1, 'sort': f'createdAt,{order}'},
            headers={
                'Authorization': f'Bearer {user_token}',
            },
        )
        response.raise_for_status()
        for events in response.json().get('_embedded', {}).values():
            if events:
                return events[0].get('createdAt')
        return None

    async def get_project_dates(self, project_uuid: str, user_token: str, project_data: dict) -> tuple[str, str]:
        # Project events are used, replies timestamps (or current time) serve as a fallback
        try:
            created = await self._get_project_event_time(project_uuid, user_token, 'asc')
            modified = await self._get_project_event_time(project_uuid, user_token, 'desc')
        except httpx.HTTPError:
            created, modified = None, None
        timestamps = mapping.Replies(project_data.get('replies') or {}).timestamps()
        now = datetime.datetime.now(datetime.UTC).isoformat()
        created = created or (timestamps[0] if timestamps else now)
        modified = modified or (timestamps[-1] if timestamps else created)
        return _to_datetime_str(created), _to_datetime_str(modified)

    async def get_madmp(self, project_uuid: str, user_token: str, client_url: str | None = None) -> dict:
        project_data = await self.get_project(project_uuid, user_token)
        mapping.check_knowledge_model(project_data)
        created, modified = await self.get_project_dates(project_uuid, user_token, project_data)
        return mapping.to_madmp(
            project_data=project_data,
            client_url=(client_url or self.default_client_url).rstrip('/'),
            created=created,
            modified=modified,
        )
