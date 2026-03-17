import type { Job } from '../../types'

export function HistoryItem({ job }: { job: Job }) {
  return <div className="card"><div className="flex justify-between items-center"><div><div className="text-[13px] text-[var(--text-primary)]">{job.input_filename}</div><div className="mono text-[10px] text-[var(--text-muted)]">{job.processing_time_seconds?.toFixed(1)}s forge · {job.created_at}</div></div><div className="flex gap-2"><button className="btn-secondary">↓ SAVE</button><button className="btn-secondary">↻ REFORGE</button></div></div></div>
}
