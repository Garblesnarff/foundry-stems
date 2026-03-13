import type { Job } from '../../types'

export function QueueItem({ job }: { job: Job & { position?: number } }) {
  return <div className="card"><div className="flex justify-between"><div><div className="text-[13px] text-[var(--text-primary)]">{job.input_filename}</div><div className="mono text-[10px] text-[var(--text-muted)]">{job.status.toUpperCase()} {job.position ? `· #${job.position}` : ''}</div></div>{job.status==='queued' && <button className="btn-secondary">X</button>}</div>{job.status==='processing' && <div className="mt-2 progress-track"><div className="progress-fill" style={{width:`${job.progress_percent}%`}} /></div>}</div>
}
