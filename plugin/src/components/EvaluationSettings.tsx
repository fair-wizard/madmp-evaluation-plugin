import { SettingsComponentProps } from '@ds-wizard/plugin-sdk/elements'
import { useRef, useState } from 'react'

import {
    DEFAULT_EVALUATION_SERVICE_URL,
    getEvaluationServiceUrl,
    REFERENCE_IMPLEMENTATION_URL,
    SettingsData,
    SUPPORTED_API_VERSION,
} from '../data/settings-data'
import { FormData } from './evaluation-project-tab/data'
import { FlashError } from './evaluation-project-tab/FlashError'
import { getFormData } from './evaluation-project-tab/requests'

export default function EvaluationSettings({
    settings,
    onSettingsChange,
}: SettingsComponentProps<SettingsData>) {
    const [testLoading, setTestLoading] = useState(false)
    const [testError, setTestError] = useState<string | null>(null)
    const [testResult, setTestResult] = useState<FormData | null>(null)
    const latestTestRef = useRef(0)

    const resetTest = () => {
        latestTestRef.current += 1
        setTestLoading(false)
        setTestError(null)
        setTestResult(null)
    }

    const handleUrlChange = (evaluationServiceUrl: string) => {
        resetTest()
        onSettingsChange({ ...settings, evaluationServiceUrl })
    }

    const handleTest = async () => {
        resetTest()
        const testId = latestTestRef.current
        const url = getEvaluationServiceUrl(settings)
        setTestLoading(true)

        try {
            const result = await getFormData(url)
            if (testId === latestTestRef.current) {
                setTestResult(result)
            }
        } catch {
            if (testId === latestTestRef.current) {
                setTestError(`Could not load benchmarks and tests from ${url}`)
            }
        } finally {
            if (testId === latestTestRef.current) {
                setTestLoading(false)
            }
        }
    }

    return (
        <div>
            <div className="form-group">
                <label htmlFor="evaluation-service-url">DMP Evaluation Service URL</label>
                <div className="input-group">
                    <input
                        id="evaluation-service-url"
                        type="url"
                        className="form-control"
                        placeholder={DEFAULT_EVALUATION_SERVICE_URL}
                        value={settings.evaluationServiceUrl}
                        onChange={(e) => handleUrlChange(e.target.value)}
                    />
                    <button
                        type="button"
                        className="btn btn-outline-secondary"
                        onClick={() => handleUrlChange(DEFAULT_EVALUATION_SERVICE_URL)}
                        disabled={settings.evaluationServiceUrl === DEFAULT_EVALUATION_SERVICE_URL}
                    >
                        Restore default
                    </button>
                </div>
                <p className="form-text text-muted">
                    Supports DMP Evaluation API specification version {SUPPORTED_API_VERSION}. See
                    the{' '}
                    <a
                        href={REFERENCE_IMPLEMENTATION_URL}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        reference implementation
                    </a>
                    .
                </p>
            </div>
            <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={handleTest}
                disabled={testLoading}
            >
                {testLoading ? <i className="fas fa-spinner fa-spin"></i> : 'Test API'}
            </button>
            {testError && (
                <div className="mt-3">
                    <FlashError message={testError} />
                </div>
            )}
            {testResult && (
                <div className="mt-3">
                    <TestResultList title="Benchmarks" items={testResult.benchmarks} />
                    <TestResultList title="Tests" items={testResult.tests} />
                </div>
            )}
        </div>
    )
}

function TestResultList({
    title,
    items,
}: {
    title: string
    items: { identifier: string; title: string }[]
}) {
    return (
        <details className="mb-3">
            <summary>
                <strong>
                    {title} ({items.length})
                </strong>
            </summary>
            <div className="list-group mt-2">
                {items.map((item) => (
                    <div key={item.identifier} className="list-group-item">
                        {item.title}
                    </div>
                ))}
            </div>
        </details>
    )
}
