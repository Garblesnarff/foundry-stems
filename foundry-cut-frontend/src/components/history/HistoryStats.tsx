import type { HistoryStats as Stats } from '../../types'

export function HistoryStats({ stats }: { stats: Stats }) {
  const cards = [
    ['SONGS FORGED', stats.lifetime.jobs_completed, 'var(--accent-amber)'],
    ['TOTAL AUDIO', `${Math.round(stats.lifetime.total_input_seconds)}s`, 'var(--accent-red)'],
    ['FORGE TIME', `${Math.round(stats.lifetime.total_processing_seconds)}s`, 'var(--accent-green)'],
    ['AVG SPEED', stats.lifetime.avg_speed_ratio.toFixed(2), 'var(--accent-blue)']
  ]
  return <div className="grid grid-cols-2 xl:grid-cols-4 gap-3">{cards.map(([l,v,c])=><div key={String(l)} className="stat-card"><div className="stat-card-label">{l}</div><div className="stat-card-value" style={{color: String(c)}}>{v}</div></div>)}</div>
}
