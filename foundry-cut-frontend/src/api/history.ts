import { api } from './client'
import type { Job, HistoryStats } from '../types'

export const getHistory = (search = '', sort = 'newest', limit = 50, offset = 0) => api<{jobs:Job[];total:number;limit:number;offset:number}>(`/history?search=${encodeURIComponent(search)}&sort=${sort}&limit=${limit}&offset=${offset}`)
export const getHistoryStats = () => api<HistoryStats>('/history/stats')
export const deleteHistoryItem = (id: string) => api<{ok:boolean}>(`/history/${id}`, { method: 'DELETE' })
export const clearHistory = () => api<{ok:boolean}>('/history', { method: 'DELETE' })
