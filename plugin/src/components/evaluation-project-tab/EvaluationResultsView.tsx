import { useMemo, useState } from 'react'

import { Evaluation, EvaluationResponse, EvaluationResult } from './data'

export function EvaluationResultsView({
    data,
    onBack,
}: {
    data: EvaluationResponse
    onBack?: () => void
}) {
    const evaluations = useMemo(() => {
        return data.evaluations || []
    }, [data.evaluations])

    const [openIds, setOpenIds] = useState<Set<string>>(
        () => new Set(evaluations.length ? [evaluations[0]!.identifier] : []),
    )

    const counts = useMemo(() => {
        return evaluations.reduce(
            (acc, e) => {
                acc[e.value] += 1
                return acc
            },
            {
                PASS: 0,
                FAIL: 0,
                ERROR: 0,
                INDERTERMINATED: 0,
                INDETERMINATE: 0,
                NOT_APPLICABLE: 0,
            } satisfies Record<EvaluationResult, number>,
        )
    }, [evaluations])

    const toggle = (id: string) => {
        setOpenIds((prev) => {
            const next = new Set(prev)
            if (next.has(id)) {
                next.delete(id)
            } else {
                next.add(id)
            }
            return next
        })
    }

    return (
        <div className="col col-detail mx-auto">
            <div className="d-flex align-items-center justify-content-between mb-3">
                <h2 className="mb-0">Evaluation Results</h2>

                {onBack && (
                    <button className="btn btn-wide btn-outline-secondary" onClick={onBack}>
                        Back
                    </button>
                )}
            </div>

            {data.message && <div className="alert alert-info">{data.message}</div>}

            {/* SUMMARY (only > 0) */}
            <div className="d-flex flex-wrap gap-2 mb-3">
                {(Object.entries(counts) as [EvaluationResult, number][])
                    .filter(([, count]) => count > 0)
                    .map(([result, count]) => (
                        <span key={result} className={badgeClass(result)}>
                            {result}: {count}
                        </span>
                    ))}
            </div>

            {evaluations.length === 0 ? (
                <div className="alert alert-secondary">No evaluations returned.</div>
            ) : (
                <div className="list-group">
                    {evaluations.map((e) => {
                        return (
                            <EvaluationView
                                evaluation={e}
                                isOpen={openIds.has(e.identifier)}
                                toggle={toggle}
                            />
                        )
                    })}
                </div>
            )}
        </div>
    )
}

function EvaluationView({
    evaluation: e,
    isOpen,
    toggle,
}: {
    evaluation: Evaluation
    isOpen: boolean
    toggle: (id: string) => void
}) {
    return (
        <div key={e.identifier} className="list-group-item">
            <div
                className="d-flex justify-content-between align-items-center"
                style={{ cursor: 'pointer' }}
                onClick={() => toggle(e.identifier)}
            >
                <div className="d-flex align-items-center gap-2">
                    <span className={badgeClass(e.value)}>
                        <i className={`${iconClass(e.value)} me-1`} />
                        {e.value}
                    </span>
                    <strong>{e.title}</strong>
                </div>

                <i className={`fas ${isOpen ? 'fa-chevron-up' : 'fa-chevron-down'}`} />
            </div>

            {isOpen && (
                <div className="mt-1">
                    {e.description && <p className="text-muted">{e.description}</p>}

                    <div className="mt-3">
                        {e.generatedAtTime && (
                            <div className="mb-3">
                                <div className="fw-semibold small">Timestamp</div>
                                <div>{formatTimestamp(e.generatedAtTime)}</div>
                            </div>
                        )}

                        {e.log && (
                            <div className="mb-3">
                                <div className="fw-semibold small">Log</div>
                                <pre className="mb-0" style={{ whiteSpace: 'pre-wrap' }}>
                                    {e.log}
                                </pre>
                            </div>
                        )}

                        {e.reportId && (
                            <div className="mb-3">
                                <div className="fw-semibold small">Report ID</div>
                                <code>{e.reportId}</code>
                            </div>
                        )}

                        {e.wasGeneratedBy && (
                            <div className="mb-3">
                                <div className="fw-semibold small">Generated by</div>
                                <code className="text-break">{e.wasGeneratedBy}</code>
                            </div>
                        )}

                        {(e.affectedElements ?? null) !== null && (
                            <div className="mb-3">
                                <div className="fw-semibold small">Affected elements</div>
                                <pre className="mb-0">{e.affectedElements?.toString()}</pre>
                            </div>
                        )}

                        {(e.completion ?? null) !== null && (
                            <div className="mb-3">
                                <div className="fw-semibold small">Completion</div>
                                <div>{e.completion}%</div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}

function badgeClass(result: EvaluationResult) {
    switch (result) {
        case 'PASS':
            return 'badge bg-success'
        case 'FAIL':
            return 'badge bg-danger'
        case 'ERROR':
            return 'badge bg-dark'
        case 'INDERTERMINATED':
            return 'badge bg-warning text-dark'
        case 'NOT_APPLICABLE':
            return 'badge bg-secondary'
        default:
            return 'badge bg-secondary'
    }
}

function iconClass(result: EvaluationResult) {
    switch (result) {
        case 'PASS':
            return 'fas fa-check-circle'
        case 'FAIL':
            return 'fas fa-times-circle'
        case 'ERROR':
            return 'fas fa-bug'
        case 'INDERTERMINATED':
            return 'fas fa-question-circle'
        case 'NOT_APPLICABLE':
            return 'fas fa-minus-circle'
        default:
            return 'fas fa-circle'
    }
}

function formatTimestamp(ts: string | null) {
    if (!ts) return null
    const d = new Date(ts)
    return Number.isNaN(d.getTime()) ? ts : d.toLocaleString()
}
