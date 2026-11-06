import { PluginMetadata } from '@ds-wizard/plugin-sdk/types'

import pkg from '../package.json' with { type: 'json' }

export const pluginMetadata: PluginMetadata = {
    uuid: '8d372e4a-6145-4863-9831-82eb0ead1195',
    name: 'maDMP Evaluation',
    description:
        'Plugin to evaluate machine-actionable Data Management Plans (maDMPs) through integration with DMP Evaluation Service.',
    version: pkg.version,
}
