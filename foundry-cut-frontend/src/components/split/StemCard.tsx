import type { StemFile } from '../../types'
import { STEM_COLORS } from '../../types'
import { WaveformDisplay } from './WaveformDisplay'

export function StemCard({ stem }: { stem: StemFile }) {
  const color = STEM_COLORS[stem.name] ?? '#E8A849'
  return <div className="card"><div className="mono text-[11px] uppercase" style={{color}}>● {stem.name}</div><WaveformDisplay color={color} active /><div className="flex items-center gap-2 mt-3"><button className="play-btn" style={{backgroundColor:`${color}33`,color}}>▶</button><button className="btn-secondary">S</button><button className="btn-secondary">M</button><input type="range" className="flex-1" defaultValue={80} /><button className="btn-secondary">↓</button></div></div>
}
