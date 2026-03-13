import { useEffect, useState } from 'react'
import { clearQueue, getJobs } from '../../api/jobs'
import type { Job } from '../../types'
import { QueueItem } from './QueueItem'

export function QueueView() {
  const [processing, setProcessing] = useState<Job | null>(null)
  const [queued, setQueued] = useState<(Job & { position?: number })[]>([])
  useEffect(() => { const load = () => void getJobs().then((d)=>{setProcessing(d.processing); setQueued(d.queued)}); load(); const i = setInterval(load, 1500); return ()=>clearInterval(i) }, [])
  return <div className="p-6 space-y-3">{processing && <QueueItem job={processing} />}{queued.map((q)=><QueueItem key={q.id} job={q} />)}<button className="btn-danger" onClick={()=>void clearQueue()}>CLEAR QUEUE</button></div>
}
