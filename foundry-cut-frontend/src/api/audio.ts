import { api, BASE } from './client'

export const stemUrl = (jobId: string, stemName: string) => `${BASE}/audio/${jobId}/${stemName}`
export const getWaveform = (jobId: string, stemName: string) => api<{stem:string;points:number[];duration_seconds:number;num_points:number}>(`/audio/${jobId}/${stemName}/waveform`)
