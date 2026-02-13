import pydantic


class EvaluationRequest(pydantic.BaseModel):
    api_url: str
    project_uuid: str
    user_token: str
    benchmark: str | None = None
    test: str | None = None


class EvaluationResponse(pydantic.BaseModel):
    ok: bool
    evaluations: list[dict] = pydantic.Field(default_factory=list)
    madmp: dict | None
    message: str | None = pydantic.Field(default=None)


class FormDataResponse(pydantic.BaseModel):
    ok: bool
    benchmarks: list[dict] = pydantic.Field(default_factory=list)
    tests: list[dict] = pydantic.Field(default_factory=list)
