import { makeJsonCodec } from '@ds-wizard/plugin-sdk/utils'
import { z } from 'zod'

export const DEFAULT_EVALUATION_SERVICE_URL = 'https://ostrails-dmp-evaluation.arisnet.ac.at'
export const SUPPORTED_API_VERSION = '1.0.0'
export const REFERENCE_IMPLEMENTATION_URL = 'https://github.com/OSTrails/DMP-Evaluation-Service'

export const SettingsDataSchema = z.object({
    evaluationServiceUrl: z.string().default(DEFAULT_EVALUATION_SERVICE_URL),
})

export type SettingsData = z.infer<typeof SettingsDataSchema>

export const DefaultSettingsData: SettingsData = {
    evaluationServiceUrl: DEFAULT_EVALUATION_SERVICE_URL,
}

export const SettingsDataCodec = makeJsonCodec(SettingsDataSchema, DefaultSettingsData)

export function getEvaluationServiceUrl(settings: SettingsData): string {
    return settings.evaluationServiceUrl.trim() || DEFAULT_EVALUATION_SERVICE_URL
}
