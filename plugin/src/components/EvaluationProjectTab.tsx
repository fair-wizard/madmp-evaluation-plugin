import { ProjectTabComponentProps } from '@ds-wizard/plugin-sdk/elements'
import { SettingsData } from '../data/settings-data'

export default function ProjectTab({
    settings,
    userSettings,
    project,
}: ProjectTabComponentProps<SettingsData, null>) {
    return <div>Project Tab</div>
}
