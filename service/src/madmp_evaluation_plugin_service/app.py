import fastapi
import fastapi.responses

from . import logic, schemas


def create_app(api_url: str | None = None) -> fastapi.FastAPI:
    api_url = api_url or ''
    api_url = api_url.rstrip('/')

    app = fastapi.FastAPI(
        title='maDMP Evaluation Plugin Service',
        description='A service to evaluate machine-actionable Data Management Plans (maDMPs).',
        version='0.1.0',
    )

    @app.get('/api/init', response_model=schemas.InitResponse)
    async def get_init() -> schemas.InitResponse:
        return await logic.init()

    @app.post('/api/evaluate', response_model=schemas.EvaluationResponse)
    async def post_evaluate(req: schemas.EvaluationRequest) -> schemas.EvaluationResponse:
        return await logic.evaluate(api_url, req)

    return app
