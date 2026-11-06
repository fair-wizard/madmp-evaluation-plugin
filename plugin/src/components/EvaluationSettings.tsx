import { SettingsComponentProps } from '@ds-wizard/plugin-sdk/elements'
import { Alert } from '@ds-wizard/plugin-sdk/ui/Alert'
import { Button } from '@ds-wizard/plugin-sdk/ui/Button'
import { TextField } from '@ds-wizard/plugin-sdk/ui/Field'
import { FormActions, FormCollapsible } from '@ds-wizard/plugin-sdk/ui/Form'
import { Stack } from '@ds-wizard/plugin-sdk/ui/Layout'
import { Link } from '@ds-wizard/plugin-sdk/ui/Link'
import { List, ListItem } from '@ds-wizard/plugin-sdk/ui/ListItem'
import { useRef, useState } from 'react'

import {
    DEFAULT_EVALUATION_SERVICE_URL,
    getEvaluationServiceUrl,
    REFERENCE_IMPLEMENTATION_URL,
    SettingsData,
    SUPPORTED_API_VERSION,
} from '../data/settings-data'
import { FormData } from './evaluation-project-tab/data'
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

    const isDefaultUrl = settings.evaluationServiceUrl === DEFAULT_EVALUATION_SERVICE_URL

    return (
        <Stack>
            <TextField
                id="evaluation-service-url"
                label="DMP Evaluation Service URL"
                type="url"
                placeholder={DEFAULT_EVALUATION_SERVICE_URL}
                value={settings.evaluationServiceUrl}
                onChange={handleUrlChange}
                hint={
                    <>
                        Supports DMP Evaluation API specification version {SUPPORTED_API_VERSION}.
                        See the{' '}
                        <Link href={REFERENCE_IMPLEMENTATION_URL} external>
                            reference implementation
                        </Link>
                        .
                    </>
                }
            />
            <FormActions>
                <Button icon="fa-plug" loading={testLoading} onClick={handleTest}>
                    Test API
                </Button>
                <Button
                    variant="ghost"
                    icon="fa-rotate-left"
                    disabledReason={
                        isDefaultUrl
                            ? { id: 'restore-default-reason', reason: 'The default URL is in use' }
                            : undefined
                    }
                    onClick={() => handleUrlChange(DEFAULT_EVALUATION_SERVICE_URL)}
                >
                    Restore default
                </Button>
            </FormActions>
            {testError && <Alert tone="danger">{testError}</Alert>}
            {testResult && (
                <Stack>
                    <Alert tone="success">
                        Loaded {testResult.benchmarks.length} benchmarks and{' '}
                        {testResult.tests.length} tests.
                    </Alert>
                    <TestResultList title="Benchmarks" items={testResult.benchmarks} />
                    <TestResultList title="Tests" items={testResult.tests} />
                </Stack>
            )}
        </Stack>
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
        <FormCollapsible label={`${title} (${items.length})`}>
            <List>
                {items.map((item) => (
                    <ListItem key={item.identifier} title={item.title} />
                ))}
            </List>
        </FormCollapsible>
    )
}
