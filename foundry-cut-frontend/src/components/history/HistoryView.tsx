import { useEffect, useState } from 'react'
import { clearHistory, getHistory, getHistoryStats } from '../../api/history'
import type { HistoryStats as Stats, Job } from '../../types'
import { HistoryFilters } from './HistoryFilters'
import { HistoryItem } from './HistoryItem'
import { HistoryStats } from './HistoryStats'

export function HistoryView() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [stats, setStats] = useState<Stats>({session:{jobs_completed:0,total_input_seconds:0,total_processing_seconds:0,avg_speed_ratio:0}, lifetime:{jobs_completed:0,total_input_seconds:0,total_processing_seconds:0,avg_speed_ratio:0}})
  const [search, setSearch] = useState('')
  const [sort, setSort] = useState('newest')
  useEffect(() => { void getHistoryStats().then(setStats) }, [])
  useEffect(() => { void getHistory(search, sort).then((d)=>setJobs(d.jobs)) }, [search, sort])
  return <div className="p-6 space-y-4"><div className="flex justify-between"><div><h1 className="title">Forge History</h1><p className="text-[var(--text-muted)] text-[12px]">{stats.lifetime.jobs_completed} songs forged</p></div><div className="flex gap-2"><button className="btn-secondary">EXPORT ALL ↓</button><button className="btn-danger" onClick={()=>void clearHistory()}>CLEAR</button></div></div><HistoryStats stats={stats} /><HistoryFilters search={search} setSearch={setSearch} sort={sort} setSort={setSort} />{jobs.map((j)=><HistoryItem key={j.id} job={j} />)}</div>
}
