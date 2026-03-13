import { patchSettings } from '../../api/settings'
import { appActions, useAppStore } from '../../stores/appStore'

export function SettingsPanel() {
  const { settingsOpen, settings } = useAppStore()
  if (!settingsOpen || !settings) return null
  const update = async (k: string, v: string | number) => {
    const res = await patchSettings({ [k]: v } as never)
    appActions.setSettings(res.settings)
  }
  return <div className="settings-panel" onClick={()=>appActions.toggleSettings()}><aside className="settings-content" onClick={(e)=>e.stopPropagation()}><div className="mono text-[10px] text-[var(--text-muted)] mb-3">SETTINGS</div><label className="block text-[12px] mb-1">Model</label><select className="select-field w-full" value={settings.model} onChange={(e)=>void update('model', e.target.value)}><option>htdemucs</option><option>htdemucs_ft</option><option>htdemucs_6s</option><option>mdx_extra</option></select><label className="block text-[12px] mt-4 mb-1">Threads</label><input className="input-field" type="number" value={settings.num_threads} onChange={(e)=>void update('num_threads', Number(e.target.value))} /></aside></div>
}
