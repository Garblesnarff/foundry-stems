import { useEffect, useState } from 'react'
import { getSettings } from '../../api/settings'
import { getJob, separateFile } from '../../api/separate'
import { useSSE } from '../../hooks/useSSE'
import { appActions, useAppStore } from '../../stores/appStore'
import type { ProgressEvent, Settings } from '../../types'
import { Dropzone } from './Dropzone'
import { ProgressPanel } from './ProgressPanel'
import { SplitSettings } from './SplitSettings'
import { StemResults } from './StemResults'

export function SplitView() {
  const { currentJob, settings } = useAppStore()
  const [progress, setProgress] = useState<ProgressEvent>({ stage: 'analyzing', percent: 0 })

  useEffect(() => { void getSettings().then(appActions.setSettings) }, [])
  useSSE(currentJob?.id ?? null, (p) => setProgress(p), () => { if (currentJob) void getJob(currentJob.id).then((j)=>appActions.setCurrentJob(j.job)) })

  const readySettings = settings ?? { model: 'htdemucs', output_format: 'wav', sample_rate: 44100, num_threads: 6, output_directory: '', auto_cleanup_days: 30 }
  const onFiles = async (files: File[]) => {
    const { job } = await separateFile(files[0], readySettings.model, readySettings.output_format, ['vocals','drums','bass','other'])
    appActions.setCurrentJob(job)
  }

  return <div className="p-6 space-y-4">{!currentJob && <Dropzone onFiles={onFiles} />}
    <SplitSettings settings={readySettings as Settings} setSettings={appActions.setSettings as (s: Settings)=>void} />
    {currentJob?.status === 'processing' && <ProgressPanel stage={progress.stage} percent={progress.percent} />}
    {currentJob?.status === 'completed' && <StemResults job={currentJob} />}
  </div>
}
