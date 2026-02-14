import json

import httpx

from . import schemas
from .evaluation_service import EvaluationServiceClient
from .wizard import WizardClient

EVALUATION_SERVICE_API_URL = 'https://ostrails-dmp-evaluation.arisnet.ac.at/'


async def prepare_form_data() -> schemas.FormDataResponse:
    async with httpx.AsyncClient() as client:
        try:
            eval_client = EvaluationServiceClient(
                api_url=EVALUATION_SERVICE_API_URL,
                client=client,
            )
            benchmarks = await eval_client.get_benchmarks()
            tests = await eval_client.get_tests()
            return schemas.FormDataResponse(
                ok=True,
                benchmarks=benchmarks,
                tests=tests,
            )
        except Exception:
            return schemas.FormDataResponse(
                ok=False,
            )


async def evaluate(req: schemas.EvaluationRequest) -> schemas.EvaluationResponse:
    madmp = None
    async with httpx.AsyncClient() as client:
        try:
            wizard = WizardClient(
                api_url=req.api_url,
                client=client,
            )
            project_data = await wizard.get_project(
                project_uuid=req.project_uuid,
                user_token=req.user_token,
            )
            madmp = wizard.to_madmp(
                project_data=project_data,
            )
            eval_client = EvaluationServiceClient(
                api_url=EVALUATION_SERVICE_API_URL,
                client=client,
            )
            evaluations = []
            if req.benchmark:
                benchmark_evaluations = await eval_client.evaluate_benchmark(
                    benchmark=req.benchmark,
                    madmp=json.dumps(madmp),
                )
                evaluations.extend(benchmark_evaluations)
            if req.test:
                test_evaluation = await eval_client.evaluate_test(
                    test=req.test,
                    madmp=json.dumps(madmp),
                )
                evaluations.append(test_evaluation)
            return schemas.EvaluationResponse(
                ok=True,
                evaluations=evaluations,
                madmp=madmp,
            )
        except Exception as e:
            return schemas.EvaluationResponse(
                ok=False,
                madmp=madmp,
                message=str(e),
            )
