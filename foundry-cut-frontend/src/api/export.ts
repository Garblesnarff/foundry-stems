import { BASE } from './client'

export async function exportStems(payload: {job_id: string; stems: string[]; format: string; mode: 'zip'|'individual'}) {
  const res = await fetch(`${BASE}/export/stems`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
  if (!res.ok) throw new Error('Export failed')
  return res.blob()
}
