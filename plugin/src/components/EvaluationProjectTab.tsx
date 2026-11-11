import { ProjectTabComponentProps } from '@ds-wizard/plugin-sdk/elements'
import { AsyncBlock } from '@ds-wizard/plugin-sdk/ui/AsyncBlock'
import { Stack } from '@ds-wizard/plugin-sdk/ui/Layout'
import { token } from '@ds-wizard/plugin-sdk/ui/tokens'
import { CSSProperties, ReactNode, useEffect, useState } from 'react'

import { getEvaluationServiceUrl, SettingsData } from '../data/settings-data'
import { EvaluationResponse, EvaluationType, FormData } from './evaluation-project-tab/data'
import { EvaluationResultsView } from './evaluation-project-tab/EvaluationResultsView'
import { EvaluationSelectionForm } from './evaluation-project-tab/EvaluationSelectionForm'
import { getFormData, postEvaluation } from './evaluation-project-tab/requests'

type View = 'loading' | 'form' | 'results' | 'error'

const contentStyle: CSSProperties = {
    inlineSize: '100%',
    maxInlineSize: token('--ui-measure-form'),
    marginInline: 'auto',
}

// The wizard pads a project tab only when a Stack is its root element
function TabContent({ children }: { children: ReactNode }) {
    return (
        <Stack>
            <Stack loose style={contentStyle}>
                {children}
            </Stack>
        </Stack>
    )
}

export default function ProjectTab({
    project,
    settings,
}: ProjectTabComponentProps<SettingsData, null>) {
    const evaluationServiceUrl = getEvaluationServiceUrl(settings)

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

                const data = await getFormData(evaluationServiceUrl)

                setFormData(data)
                setView('form')
            } catch (error: Error | unknown) {
                console.log('Error loading form data:', error)
                setLoadingError('Failed to load form data')
                setView('error')
            }
        }
        load()
    }, [evaluationServiceUrl])

    const handleSubmit = async (evaluationType: EvaluationType, id: string) => {
        try {
            setEvaluationError(null)
            setEvaluationLoading(true)

            const result = await postEvaluation(project, evaluationServiceUrl, evaluationType, id)

            if (result.ok) {
                setEvaluationResult(result)
                setView('results')
            } else {
                setEvaluationError(result.message || 'Evaluation failed')
                setView('form')
            }
        } catch (error: Error | unknown) {
            setEvaluationError(error instanceof Error ? error.message : 'Evaluation failed')
            setView('form')
        } finally {
            setEvaluationLoading(false)
        }
    }

    if (view === 'loading' || view === 'error') {
        return (
            <TabContent>
                <AsyncBlock
                    loading={view === 'loading'}
                    error={loadingError ?? 'An unknown error occurred'}
                />
            </TabContent>
        )
    }

    return (
        <TabContent>
            {view === 'results' && evaluationResult ? (
                <EvaluationResultsView data={evaluationResult} onBack={() => setView('form')} />
            ) : (
                <EvaluationSelectionForm
                    formData={formData}
                    evaluationLoading={evaluationLoading}
                    evaluationError={evaluationError}
                    onSubmit={handleSubmit}
                />
            )}
        </TabContent>
    )
}
