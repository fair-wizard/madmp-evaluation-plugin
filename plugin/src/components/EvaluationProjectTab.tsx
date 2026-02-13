import { ProjectTabComponentProps } from '@ds-wizard/plugin-sdk/elements'
import { useEffect, useState } from 'react'
import { z } from 'zod'

import { SettingsData } from '../data/settings-data'

type View = 'loading' | 'form' | 'submitting' | 'results' | 'error'

type EvaluationType = 'benchmarks' | 'tests'

const BenchmarkSchema = z.object({
    benchmarkId: z.string(),
    title: z.string(),
})

const TestSchema = z.object({
    id: z.string(),
    title: z.string(),
})

type Benchmark = z.infer<typeof BenchmarkSchema>
type Test = z.infer<typeof TestSchema>

const FormDataSchema = z.object({
    benchmarks: z.array(BenchmarkSchema),
    tests: z.array(TestSchema),
})

type FormData = z.infer<typeof FormDataSchema>

type EvaluationRequest = {
    apiUrl: string | null
    projectUuid: string | null
    userToken: string | null
    benchmark: string | null
    test: string | null
}

const EvaluationResultSchema = z.object({
    ok: z.boolean(),
    message: z.string().optional(),
    // Define other response fields as needed
})

type EvaluationResult = z.infer<typeof EvaluationResultSchema>

export default function ProjectTab({
    settings,
    project,
}: ProjectTabComponentProps<SettingsData, null>) {
    const [view, setView] = useState<View>('loading')
    const [loadingError, setLoadingError] = useState<string | null>(null)
    const [formData, setFormData] = useState<FormData>({ benchmarks: [], tests: [] })
    const [evaluationError, setEvaluationError] = useState<string | null>(null)
    const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null)

    useEffect(() => {
        const load = async () => {
            try {
                setLoadingError(null)
                setView('loading')

                const data = await requestJson(`${__API_URL__}/form-data`, FormDataSchema)

                setFormData(data)
                setView('form')
            } catch {
                setLoadingError('Failed to load form data')
                setView('error')
            }
        }

        load()
    }, [])

    if (view === 'loading') return <Loader />
    if (view === 'error') return <ErrorMessage message={loadingError} />

    const handleSubmit = async (evaluationType: EvaluationType, id: string) => {
        try {
            setEvaluationError(null)
            setView('submitting')

            const sessionString = localStorage.getItem('session/wizard')
            const session = sessionString ? JSON.parse(sessionString) : null

            const apiUrl = session?.apiUrl || null
            const token = session?.token?.token || null

            const evaluationRequest: EvaluationRequest = {
                apiUrl: apiUrl,
                projectUuid: project?.uuid || null,
                userToken: token,
                benchmark: evaluationType === 'benchmarks' ? id : null,
                test: evaluationType === 'tests' ? id : null,
            }

            const result = await requestJson(`${__API_URL__}/evaluation`, EvaluationResultSchema, {
                method: 'POST',
                body: evaluationRequest,
            })

            if (result.ok) {
                setEvaluationResult(result)
                setView('results')
            } else {
                setEvaluationError(result.message ?? 'Evaluation failed')
                setView('form')
            }
        } catch {
            setEvaluationError('Evaluation failed')
            setView('form')
        }
    }

    return (
        <EvaluationSelectionForm
            formData={formData}
            evaluationError={evaluationError}
            onSubmit={handleSubmit}
        />
    )
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
        // const msg =
        //     (payload &&
        //         typeof payload === 'object' &&
        //         'message' in payload &&
        //         (payload as any).message) ||
        //     `HTTP ${res.status} ${res.statusText}`
        throw new Error('Request failed')
    }

    const parsed = schema.safeParse(payload)
    if (!parsed.success) {
        // You can log parsed.error.format() for debugging
        throw new Error('Unexpected response from server (schema mismatch)')
    }

    return parsed.data
}

function Loader() {
    return (
        <div className="page-loader">
            <i className="fas fa-spinner fa-spin"></i>
            <div>Loading...</div>
        </div>
    )
}

function ErrorMessage({ message }: { message: string | null }) {
    return (
        <div className="Projects__Detail__Content">
            <div className="col col-detail mx-auto">
                <FlashError message={message ?? 'An unknown error occurred'} />
            </div>
        </div>
    )
}

function EvaluationSelectionForm({
    formData,
    evaluationError,
    onSubmit,
}: {
    formData: FormData
    evaluationError: string | null
    onSubmit: (evaluationType: EvaluationType, id: string) => void
}) {
    const [selectedTab, setSelectedTab] = useState<EvaluationType>('benchmarks')
    const [selectedId, setSelectedId] = useState<string>('')

    const evaluationErrorMessage = evaluationError ? <FlashError message={evaluationError} /> : null

    const content =
        selectedTab === 'benchmarks' ? (
            <div className="form-group">
                <label htmlFor="benchmark-select">Select Benchmark</label>
                <select
                    id="benchmark-select"
                    className="form-select"
                    value={selectedId}
                    onChange={(e) => setSelectedId(e.target.value)}
                >
                    <option value="">Choose a benchmark...</option>
                    {formData.benchmarks.map((b) => (
                        <option key={b.benchmarkId} value={b.benchmarkId}>
                            {b.title}
                        </option>
                    ))}
                </select>
            </div>
        ) : (
            <div className="form-group">
                <label htmlFor="test-select">Select Test</label>
                <select
                    id="test-select"
                    className="form-select"
                    value={selectedId}
                    onChange={(e) => setSelectedId(e.target.value)}
                >
                    <option value="">Choose a test...</option>
                    {formData.tests.map((t) => (
                        <option key={t.id} value={t.id}>
                            {t.title}
                        </option>
                    ))}
                </select>
            </div>
        )

    return (
        <div className="Projects__Detail__Content">
            <div className="col col-detail mx-auto">
                <div className="d-flex justify-content-between align-items-center mb-3">
                    <h2>maDMP Evaluation</h2>
                </div>
                {evaluationErrorMessage}
                <div>
                    <ul className="nav nav-underline-tabs nav-underline-tabs-full border-bottom mb-3">
                        <li className="nav-item">
                            <button
                                className={`nav-link ${selectedTab === 'benchmarks' ? 'active' : ''}`}
                                onClick={() => setSelectedTab('benchmarks')}
                            >
                                <i className="fas fa-list-check"></i>
                                Benchmarks
                            </button>
                        </li>
                        <li className="nav-item">
                            <button
                                className={`nav-link ${selectedTab === 'tests' ? 'active' : ''}`}
                                onClick={() => setSelectedTab('tests')}
                            >
                                <i className="far fa-circle-check"></i>
                                Tests
                            </button>
                        </li>
                    </ul>
                    {content}
                    <div className="mt-4 pt-4 border-top">
                        <button
                            className="btn btn-wide btn-primary"
                            onClick={() => onSubmit(selectedTab, selectedId)}
                        >
                            Evaluate
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

function FlashError({ message }: { message: string }) {
    return (
        <div className="alert alert-danger d-flex align-items-baseline">
            <i className="fas fa-exclamation-circle"></i>
            <div className="ms-2">{message}</div>
        </div>
    )
}
