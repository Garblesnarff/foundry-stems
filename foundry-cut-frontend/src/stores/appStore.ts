import { useSyncExternalStore } from 'react'
import type { Job, Settings } from '../types'

type State = { tab: 'split'|'queue'|'history'; currentJob: Job | null; settings: Settings | null; settingsOpen: boolean }
let state: State = { tab: 'split', currentJob: null, settings: null, settingsOpen: false }
const listeners = new Set<() => void>()

function setState(partial: Partial<State>) { state = { ...state, ...partial }; listeners.forEach((l) => l()) }

export const appActions = {
  setTab: (tab: State['tab']) => setState({ tab }),
  setCurrentJob: (currentJob: Job | null) => setState({ currentJob }),
  setSettings: (settings: Settings) => setState({ settings }),
  toggleSettings: () => setState({ settingsOpen: !state.settingsOpen })
}

export function useAppStore() {
  return useSyncExternalStore((cb) => { listeners.add(cb); return () => listeners.delete(cb) }, () => state)
}
