import { ProjectTabComponentProps } from '@ds-wizard/plugin-sdk/elements'
import { useEffect, useState } from 'react'

import { SettingsData } from '../data/settings-data'
import { EvaluationResponse, EvaluationType, FormData } from './evaluation-project-tab/data'
import { ErrorMessage } from './evaluation-project-tab/ErrorMessage'
import { EvaluationResultsView } from './evaluation-project-tab/EvaluationResultsView'
import { EvaluationSelectionForm } from './evaluation-project-tab/EvaluationSelectionForm'
import { Loader } from './evaluation-project-tab/Loader'
import { getFormData, postEvaluation } from './evaluation-project-tab/requests'

type View = 'loading' | 'form' | 'results' | 'error'

export default function ProjectTab({ project }: ProjectTabComponentProps<SettingsData, null>) {
    const [view, setView] = useState<View>('loading')
    const [loadingError, setLoadingError] = useState<string | null>(null)

    const [formData, setFormData] = useState<FormData>({ benchmarks: [], tests: [] })

    const [evaluationLoading, setEvaluationLoading] = useState(false)
    const [evaluationError, setEvaluationError] = useState<string | null>(null)
    const [evaluationResult, setEvaluationResult] = useState<EvaluationResponse | null>(null)

    useEffect(() => {
        const load = async () => {
            try {
                setLoadingError(null)
                setView('loading')

                const data = await getFormData()

                setFormData(data)
                setView('form')
            } catch {
                setLoadingError('Failed to load form data')
                setView('error')
            }
        }
        load()
    }, [])

    const handleSubmit = async (evaluationType: EvaluationType, id: string) => {
        try {
            setEvaluationError(null)
            setEvaluationLoading(true)

            const result = await postEvaluation(project, evaluationType, id)

            if (result.ok) {
                setEvaluationResult(result)
                setView('results')
            } else {
                setEvaluationError(result.message ?? 'Evaluation failed')
                setView('form')
            }
        } catch (error: Error | unknown) {
            setEvaluationError(error instanceof Error ? error.message : 'Evaluation failed')
            setView('form')
        } finally {
            setEvaluationLoading(false)
        }
    }

    if (view === 'loading') return <Loader />
    if (view === 'error') return <ErrorMessage message={loadingError} />
    if (view === 'results' && evaluationResult) {
        return <EvaluationResultsView data={evaluationResult} onBack={() => setView('form')} />
    }

    return (
        <EvaluationSelectionForm
            formData={formData}
            evaluationLoading={evaluationLoading}
            evaluationError={evaluationError}
            onSubmit={handleSubmit}
        />
    )
}
