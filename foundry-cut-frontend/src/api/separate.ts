import { api, BASE } from './client'
import type { Job } from '../types'

export async function separateFile(file: File, model: string, output_format: string, stems: string[]) {
  const fd = new FormData(); fd.append('file', file); fd.append('model', model); fd.append('output_format', output_format); fd.append('stems', JSON.stringify(stems))
  const res = await fetch(`${BASE}/separate`, { method: 'POST', body: fd })
  if (!res.ok) throw new Error('Failed to queue separation')
  return res.json() as Promise<{ job: Job }>
}
export const getJob = (id: string) => api<{job: Job}>(`/separate/${id}`)
export const cancelJob = (id: string) => api<{ok:boolean}>(`/separate/${id}`, { method: 'DELETE' })
