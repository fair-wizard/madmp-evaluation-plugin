import { PluginBuilder } from '@ds-wizard/plugin-sdk/core'
import { Plugin } from '@ds-wizard/plugin-sdk/types'

import { SettingsDataCodec } from './data/settings-data'
import { pluginMetadata } from './metadata'
import { makeNullCodec } from '@ds-wizard/plugin-sdk'
import EvaluationProjectTab from './components/EvaluationProjectTab'

export default function (settingsInput: unknown, _userSettingsInput: unknown): Plugin {
    // Use settings for plugin initialization or delete
    // If you don't use settings change function arguments to _settingsInput and _userSettingsInput
    const _settings = SettingsDataCodec.parseOrInit(settingsInput)

    const plugin: Plugin = PluginBuilder.create(pluginMetadata, SettingsDataCodec, makeNullCodec())
        .addProjectTab(
            'fas fa-clipboard-check',
            'maDMP Evaluation',
            'madmp-evaluation',
            'x-madmp-evaluation-project-tab',
            EvaluationProjectTab,
            ['dsw:root:^2.7'],
        )
        .addProjectAction(
            'Action Name',
            'x-plugin-name-project-action', // web component name
            EvaluationProjectTab, // React component with plugin functionality
            ['dsw:root:^2'], // (optional) list of supported knowledge models
        )
        .createPlugin()

    return plugin
}
