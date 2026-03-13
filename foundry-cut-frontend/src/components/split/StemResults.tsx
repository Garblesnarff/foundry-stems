import type { Job } from '../../types'
import { StemCard } from './StemCard'
import { ForgeButton } from '../shared/ForgeButton'

export function StemResults({ job }: { job: Job }) {
  return <div className="space-y-4 animate-[fadeIn_0.2s_ease]"><div className="grid grid-cols-2 xl:grid-cols-4 gap-3">{job.stem_files?.map((s) => <StemCard key={s.id} stem={s} />)}</div><ForgeButton>FORGE STEMS ↓</ForgeButton></div>
}
