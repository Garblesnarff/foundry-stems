const BASE = 'http://localhost:3457/api/v1'

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init)
  if (!res.ok) {
    let msg = `HTTP ${res.status}`
    try { const data = await res.json(); msg = data?.detail?.message ?? data?.message ?? msg } catch {}
    throw new Error(msg)
  }
  return res.json() as Promise<T>
}

export { BASE }
