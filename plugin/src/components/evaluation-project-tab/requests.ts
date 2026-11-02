import { ProjectData } from '@ds-wizard/plugin-sdk'
import { getApiUrlAndToken } from '@ds-wizard/plugin-sdk/requests'
import { z } from 'zod'

import {
    EvaluationRequest,
    EvaluationResponse,
    EvaluationResponseSchema,
    EvaluationType,
    FormData,
    FormDataResponseSchema,
} from './data'

export async function getFormData(evaluationServiceUrl: string): Promise<FormData> {
    const query = new URLSearchParams({ evaluationServiceUrl })
    const { ok, benchmarks, tests } = await requestJson(
        `${__API_URL__}/form-data?${query}`,
        FormDataResponseSchema,
    )

    if (!ok) {
        throw new Error('Failed to load data from DMP Evaluation Service')
    }

    return { benchmarks, tests }
}

export async function postEvaluation(
    project: ProjectData | null,
    evaluationServiceUrl: string,
    evaluationType: EvaluationType,
    id: string,
): Promise<EvaluationResponse> {
    const { apiUrl, token } = getApiUrlAndToken()

    const evaluationRequest: EvaluationRequest = {
        apiUrl: apiUrl,
        projectUuid: project?.uuid || null,
        userToken: token,
        evaluationServiceUrl,
        benchmark: evaluationType === 'benchmarks' ? id : null,
        test: evaluationType === 'tests' ? id : null,
    }

    return await requestJson(`${__API_URL__}/evaluation`, EvaluationResponseSchema, {
        method: 'POST',
        body: evaluationRequest,
    })
}

async function requestJson<TSchema extends z.ZodTypeAny>(
    url: string,
    schema: TSchema,
    init: { method?: string; headers?: Record<string, string>; body?: unknown } = {},
): Promise<z.infer<TSchema>> {
    const res = await fetch(url, {
        method: init.method ?? (init.body ? 'POST' : 'GET'),
        headers: {
            Accept: 'application/json',
            ...(init.body ? { 'Content-Type': 'application/json' } : {}),
            ...(init.headers ?? {}),
        },
        body: init.body ? JSON.stringify(init.body) : undefined,
    })

    const isJson = (res.headers.get('content-type') || '').includes('application/json')
    const payload = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null)

    if (!res.ok) {
        throw new Error('Request failed')
    }

    const parsed = schema.safeParse(payload)
    if (!parsed.success) {
        console.log('Schema validation error:', parsed.error)
        throw new Error('Unexpected response from server (schema mismatch)')
    }

    return parsed.data
}
