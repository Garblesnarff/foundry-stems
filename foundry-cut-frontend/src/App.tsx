import { StatusBar } from './components/layout/StatusBar'
import { TitleBar } from './components/layout/TitleBar'
import { HistoryView } from './components/history/HistoryView'
import { QueueView } from './components/queue/QueueView'
import { SettingsPanel } from './components/settings/SettingsPanel'
import { SplitView } from './components/split/SplitView'
import { useAppStore } from './stores/appStore'

export default function App() {
  const { tab } = useAppStore()
  return <div className="h-screen w-screen flex flex-col bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans"><TitleBar /><main className="flex-1 overflow-auto">{tab==='split' && <SplitView />}{tab==='queue' && <QueueView />}{tab==='history' && <HistoryView />}</main><StatusBar /><SettingsPanel /></div>
}
