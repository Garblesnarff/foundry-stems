export function AudioPlayer({ current, total }: { current: string; total: string }) {
  return <div className="card"><div className="flex items-center gap-3"><button className="play-btn active">❚❚</button><div className="progress-track flex-1"><div className="progress-fill" style={{width:'32%'}} /></div><span className="mono text-[10px] text-[var(--text-muted)]">{current} / {total}</span></div></div>
}
