import { Alert } from '@ds-wizard/plugin-sdk/ui/Alert'
import { Badge, BadgeTone } from '@ds-wizard/plugin-sdk/ui/Badge'
import { Button, IconButton } from '@ds-wizard/plugin-sdk/ui/Button'
import { DescriptionList, DescriptionListItem } from '@ds-wizard/plugin-sdk/ui/DescriptionList'
import { EmptyState } from '@ds-wizard/plugin-sdk/ui/EmptyState'
import { Inline, Stack } from '@ds-wizard/plugin-sdk/ui/Layout'
import { List, ListItem } from '@ds-wizard/plugin-sdk/ui/ListItem'
import { Body, Code, Muted, Title } from '@ds-wizard/plugin-sdk/ui/Text'
import { token } from '@ds-wizard/plugin-sdk/ui/tokens'
import { CSSProperties, useMemo, useState } from 'react'

import { Evaluation, EvaluationResponse, EvaluationResult } from './data'

const preStyle: CSSProperties = {
    margin: 0,
    padding: token('--ui-space-3'),
    maxHeight: '16rem',
    overflow: 'auto',
    whiteSpace: 'pre-wrap',
    borderRadius: token('--ui-radius-control'),
    background: token('--ui-surface-sunken'),
    color: token('--ui-text'),
    fontSize: token('--ui-text-body-sm'),
}

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
        <Stack loose>
            <Inline align="between">
                <Title>Evaluation Results</Title>
                {onBack && (
                    <Button icon="fa-arrow-left" onClick={onBack}>
                        Back
                    </Button>
                )}
            </Inline>

            {data.message && <Alert tone="info">{data.message}</Alert>}

            <Inline>
                {(Object.entries(counts) as [EvaluationResult, number][])
                    .filter(([, count]) => count > 0)
                    .map(([result, count]) => (
                        <Badge key={result} tone={resultTone(result)} icon={resultIcon(result)}>
                            {result}: {count}
                        </Badge>
                    ))}
            </Inline>

            {evaluations.length === 0 ? (
                <EmptyState
                    title="No evaluations"
                    description="The evaluation service returned no evaluations."
                />
            ) : (
                <List>
                    {evaluations.map((e) => (
                        <EvaluationView
                            key={e.identifier}
                            evaluation={e}
                            isOpen={openIds.has(e.identifier)}
                            toggle={toggle}
                        />
                    ))}
                </List>
            )}
        </Stack>
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
        <ListItem
            title={e.title}
            icon={
                <Badge tone={resultTone(e.value)} icon={resultIcon(e.value)}>
                    {e.value}
                </Badge>
            }
            actions={
                <IconButton
                    icon={isOpen ? 'fa-chevron-up' : 'fa-chevron-down'}
                    label={isOpen ? 'Hide details' : 'Show details'}
                    variant="ghost"
                    pressed={isOpen}
                    onClick={() => toggle(e.identifier)}
                />
            }
            detail={isOpen ? <EvaluationDetail evaluation={e} /> : undefined}
        />
    )
}

function EvaluationDetail({ evaluation: e }: { evaluation: Evaluation }) {
    const items: DescriptionListItem[] = []

    if (e.generatedAtTime) {
        items.push({ term: 'Timestamp', description: formatTimestamp(e.generatedAtTime) })
    }
    if (e.log) {
        items.push({ term: 'Log', description: <Preformatted>{e.log}</Preformatted> })
    }
    if (e.reportId) {
        items.push({ term: 'Report ID', description: <Code>{e.reportId}</Code> })
    }
    if (e.wasGeneratedBy) {
        items.push({ term: 'Generated by', description: <Code>{e.wasGeneratedBy}</Code> })
    }
    if ((e.affectedElements ?? null) !== null) {
        items.push({
            term: 'Affected elements',
            description: <Preformatted>{e.affectedElements?.toString()}</Preformatted>,
        })
    }
    if ((e.completion ?? null) !== null) {
        items.push({ term: 'Completion', description: `${e.completion}%` })
    }

    return (
        <Stack>
            {e.description && (
                <Body>
                    <Muted>{e.description}</Muted>
                </Body>
            )}
            {items.length > 0 && <DescriptionList items={items} />}
        </Stack>
    )
}

function Preformatted({ children }: { children: string | undefined }) {
    return <pre style={preStyle}>{children}</pre>
}

function resultTone(result: EvaluationResult): BadgeTone {
    switch (result) {
        case 'PASS':
            return 'success'
        case 'FAIL':
            return 'danger'
        case 'ERROR':
            return 'inverse'
        case 'INDERTERMINATED':
        case 'INDETERMINATE':
            return 'warning'
        default:
            return 'neutral'
    }
}

function resultIcon(result: EvaluationResult) {
    switch (result) {
        case 'PASS':
            return 'fa-check-circle'
        case 'FAIL':
            return 'fa-times-circle'
        case 'ERROR':
            return 'fa-bug'
        case 'INDERTERMINATED':
        case 'INDETERMINATE':
            return 'fa-question-circle'
        case 'NOT_APPLICABLE':
            return 'fa-minus-circle'
        default:
            return 'fa-circle'
    }
}

function formatTimestamp(ts: string) {
    const d = new Date(ts)
    return Number.isNaN(d.getTime()) ? ts : d.toLocaleString()
}
