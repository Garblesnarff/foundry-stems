import { api } from './client'
import type { Settings } from '../types'

export const getSettings = () => api<Settings>('/settings')
export const patchSettings = (payload: Partial<Settings>) => api<{accepted: boolean; settings: Settings}>('/settings', { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
