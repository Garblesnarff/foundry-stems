import { useEffect } from 'react'
import { BASE } from '../api/client'
import type { ProgressEvent } from '../types'

export function useSSE(jobId: string | null, onProgress: (p: ProgressEvent) => void, onComplete: () => void) {
  useEffect(() => {
    if (!jobId) return
    const es = new EventSource(`${BASE}/separate/${jobId}/progress`)
    es.addEventListener('progress', (e) => onProgress(JSON.parse((e as MessageEvent).data)))
    es.addEventListener('complete', () => { onComplete(); es.close() })
    es.addEventListener('error', () => es.close())
    return () => es.close()
  }, [jobId, onProgress, onComplete])
}
