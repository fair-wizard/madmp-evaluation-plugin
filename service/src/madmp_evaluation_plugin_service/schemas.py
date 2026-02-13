import pydantic


def to_camel(s: str) -> str:
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid',
    )


class EvaluationRequest(BaseModel):
    api_url: str
    project_uuid: str
    user_token: str
    benchmark: str | None = None
    test: str | None = None


class EvaluationResponse(BaseModel):
    ok: bool
    evaluations: list[dict] = pydantic.Field(default_factory=list)
    madmp: dict | None
    message: str | None = pydantic.Field(default=None)


class FormDataResponse(BaseModel):
    ok: bool
    benchmarks: list[dict] = pydantic.Field(default_factory=list)
    tests: list[dict] = pydantic.Field(default_factory=list)
