import type { Settings } from '../../types'

export function SplitSettings({ settings, setSettings }: { settings: Settings; setSettings: (v: Settings) => void }) {
  const toggleStem = () => {}
  return <div className="flex flex-wrap gap-3"><select className="select-field" value={settings.model} onChange={(e)=>setSettings({...settings, model:e.target.value})}><option>htdemucs</option><option>htdemucs_ft</option><option>htdemucs_6s</option><option>mdx_extra</option></select><select className="select-field" value={settings.output_format} onChange={(e)=>setSettings({...settings, output_format:e.target.value})}><option>wav</option><option>mp3</option><option>flac</option></select><button className="btn-secondary" onClick={toggleStem}>STEMS: ALL</button></div>
}
