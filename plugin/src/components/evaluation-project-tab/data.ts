import { z } from 'zod'

export type EvaluationType = 'benchmarks' | 'tests'

export const BenchmarkSchema = z.object({
    benchmarkId: z.string(),
    title: z.string(),
    description: z.string(),
})

export const TestSchema = z.object({
    id: z.string(),
    title: z.string(),
    description: z.string(),
})

// export type Benchmark = z.infer<typeof BenchmarkSchema>
// export type Test = z.infer<typeof TestSchema>

export const FormDataSchema = z.object({
    benchmarks: z.array(BenchmarkSchema),
    tests: z.array(TestSchema),
})

export type FormData = z.infer<typeof FormDataSchema>

export type EvaluationRequest = {
    apiUrl: string | null
    projectUuid: string | null
    userToken: string | null
    benchmark: string | null
    test: string | null
}

export const EvaluationResultSchema = z.enum([
    'PASS',
    'FAIL',
    'ERROR',
    'INDERTERMINATED',
    'NOT_APPLICABLE',
])

export const EvaluationSchema = z.object({
    evaluationId: z.string(),

    title: z.string(),
    result: EvaluationResultSchema,
    details: z.string(),
    timestamp: z.iso.datetime(), // date-time string
    log: z.string(),

    reportId: z.string().optional(),

    affectedElements: z.string().nullable().optional(),
    completion: z.number().int().nullable().optional(), // int32

    generated: z.string().optional(),
    outputFromTest: z.string().optional(),
})

export const EvaluationResponseSchema = z.object({
    ok: z.boolean(),
    message: z.string().nullable(),
    evaluations: z.array(EvaluationSchema),
    madmp: z.object({ dmp: z.unknown() }).optional(),
})

export type Evaluation = z.infer<typeof EvaluationSchema>
export type EvaluationResponse = z.infer<typeof EvaluationResponseSchema>
export type EvaluationResult = z.infer<typeof EvaluationResultSchema>
