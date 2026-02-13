import { useState } from 'react'

import { EvaluationType, FormData } from './data'
import { FlashError } from './FlashError'

export function EvaluationSelectionForm({
    formData,
    evaluationError,
    evaluationLoading,
    onSubmit,
}: {
    formData: FormData
    evaluationError: string | null
    evaluationLoading: boolean
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
                <p className="text-muted mt-2">
                    {formData.benchmarks.find((b) => b.benchmarkId === selectedId)?.description}
                </p>
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
                <p className="text-muted mt-2">
                    {formData.tests.find((t) => t.id === selectedId)?.description}
                </p>
            </div>
        )

    return (
        <div className="Projects__Detail__Content">
            <div className="col col-detail mx-auto">
                <div className="d-flex justify-content-between align-items-center mb-3">
                    <h2>Evaluate</h2>
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
                            disabled={evaluationLoading || !selectedId}
                        >
                            {evaluationLoading ? (
                                <i className="fas fa-spinner fa-spin"></i>
                            ) : (
                                'Evaluate'
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
