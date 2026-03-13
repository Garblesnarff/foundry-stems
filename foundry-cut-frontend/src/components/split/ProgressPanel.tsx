import { EmberParticles } from '../shared/EmberParticles'

export function ProgressPanel({ stage, percent }: { stage: string; percent: number }) {
  return <div className="card relative overflow-hidden animate-[glow_2s_ease-in-out_infinite_alternate]"><EmberParticles /><div className="relative z-10"><div className="mono text-[10px] text-[var(--text-muted)] mb-3">Forging stems...</div><div className="progress-track"><div className="progress-fill" style={{width:`${percent}%`}} /></div><div className="flex justify-between mono text-[10px] mt-2 text-[var(--text-secondary)]"><span>{stage || 'analyzing'}</span><span>{Math.round(percent)}%</span></div></div></div>
}
