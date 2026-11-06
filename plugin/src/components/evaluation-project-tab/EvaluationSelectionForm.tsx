import { Alert } from '@ds-wizard/plugin-sdk/ui/Alert'
import { Button } from '@ds-wizard/plugin-sdk/ui/Button'
import { SelectField } from '@ds-wizard/plugin-sdk/ui/Field'
import { FormActions } from '@ds-wizard/plugin-sdk/ui/Form'
import { Stack } from '@ds-wizard/plugin-sdk/ui/Layout'
import { TabPanel, Tabs } from '@ds-wizard/plugin-sdk/ui/Tabs'
import { Title } from '@ds-wizard/plugin-sdk/ui/Text'
import { useState } from 'react'

import { EvaluationType, FormData } from './data'

const TABS_ID = 'madmp-evaluation-type'

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

    const isBenchmarks = selectedTab === 'benchmarks'
    const items = isBenchmarks ? formData.benchmarks : formData.tests
    const selected = items.find((item) => item.identifier === selectedId)

    const selectTab = (tab: string) => {
        setSelectedTab(tab as EvaluationType)
        setSelectedId('')
    }

    return (
        <Stack loose>
            <Title>Evaluate</Title>
            {evaluationError && <Alert tone="danger">{evaluationError}</Alert>}
            <Tabs
                id={TABS_ID}
                label="Evaluation type"
                full
                active={selectedTab}
                onSelect={selectTab}
                tabs={[
                    { id: 'benchmarks', label: 'Benchmarks', icon: 'fa-list-check' },
                    { id: 'tests', label: 'Tests', icon: 'far fa-circle-check' },
                ]}
            />
            <TabPanel tabsId={TABS_ID} label={isBenchmarks ? 'Benchmarks' : 'Tests'}>
                <SelectField
                    label={isBenchmarks ? 'Benchmark' : 'Test'}
                    value={selectedId}
                    onChange={setSelectedId}
                    hint={selected?.description}
                    options={[
                        {
                            value: '',
                            label: isBenchmarks ? 'Choose a benchmark…' : 'Choose a test…',
                        },
                        ...items.map((item) => ({ value: item.identifier, label: item.title })),
                    ]}
                />
            </TabPanel>
            <FormActions>
                <Button
                    variant="primary"
                    loading={evaluationLoading}
                    disabled={!selectedId}
                    onClick={() => onSubmit(selectedTab, selectedId)}
                >
                    Evaluate
                </Button>
            </FormActions>
        </Stack>
    )
}
