import { useAppStore } from '../../stores/appStore'

export function StatusBar() {
  const { currentJob } = useAppStore()
  return <footer className="h-8 border-t border-[var(--border)] px-4 flex items-center justify-between text-[10px] mono text-[var(--text-dim)]"><span>Powered by Demucs</span><span>{currentJob ? `${currentJob.status.toUpperCase()} · ${Math.round(currentJob.progress_percent ?? 0)}%` : 'Ready to forge'}</span></footer>
}
