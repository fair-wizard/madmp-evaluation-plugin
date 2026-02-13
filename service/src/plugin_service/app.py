import fastapi
import fastapi.responses


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI(title='Plugin Service', version='1.0.0')

    @app.get('/health')
    async def health_check() -> fastapi.responses.JSONResponse:
        return fastapi.responses.JSONResponse(content={'status': 'healthy'})

    return app
