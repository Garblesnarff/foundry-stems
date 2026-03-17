import { api, BASE } from './client'
import type { Job } from '../types'

export const getJobs = () => api<{ processing: Job | null; queued: (Job & { position?: number })[] }>('/jobs')
export const clearQueue = () => api<{cleared:number}>('/jobs/queue', { method: 'DELETE' })
export async function batchFiles(files: File[], model: string, output_format: string) {
  const fd = new FormData(); files.forEach((f) => fd.append('files', f)); fd.append('model', model); fd.append('output_format', output_format)
  const res = await fetch(`${BASE}/jobs/batch`, { method: 'POST', body: fd })
  if (!res.ok) throw new Error('Batch failed')
  return res.json() as Promise<{jobs: Job[]}>
}
