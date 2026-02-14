import fastapi
import fastapi.middleware.cors

from . import logic, schemas


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        title='maDMP Evaluation Plugin Service',
        description='A service to evaluate machine-actionable Data Management Plans (maDMPs).',
        version='0.1.0',
    )
    app.add_middleware(
        middleware_class=fastapi.middleware.cors.CORSMiddleware,  # type: ignore
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.get('/form-data', response_model=schemas.FormDataResponse)
    async def get_form_data() -> schemas.FormDataResponse:
        return await logic.prepare_form_data()

    @app.post('/evaluation', response_model=schemas.EvaluationResponse)
    async def post_evaluation(req: schemas.EvaluationRequest) -> schemas.EvaluationResponse:
        return await logic.evaluate(req)

    return app
