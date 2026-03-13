export interface Job {
  id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';
  input_filename: string;
  model: string;
  stems: string[];
  output_format: string;
  input_duration_seconds: number | null;
  input_sample_rate: number | null;
  input_channels: number | null;
  progress_percent: number;
  progress_stage: string | null;
  processing_time_seconds: number | null;
  error_message: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  stem_files?: StemFile[];
}
export interface StemFile { id: string; name: string; format: string; duration_seconds: number; file_size_bytes: number; waveform?: number[]; }
export interface StemPlaybackState { name: string; color: string; playing: boolean; soloed: boolean; muted: boolean; volume: number; }
export interface HistoryStats { session: { jobs_completed: number; total_input_seconds: number; total_processing_seconds: number; avg_speed_ratio: number; }; lifetime: { jobs_completed: number; total_input_seconds: number; total_processing_seconds: number; avg_speed_ratio: number; }; }
export interface Settings { model: string; output_format: string; sample_rate: number; num_threads: number; output_directory: string; auto_cleanup_days: number; }
export interface ProgressEvent { stage: 'analyzing' | 'separating' | 'encoding' | 'complete'; percent: number; }
export interface HealthStatus { status: 'loading' | 'ready' | 'processing' | 'error'; model: string; model_loaded: boolean; processing: boolean; current_job_id: string | null; queue_length: number; }
export const STEM_COLORS: Record<string, string> = { vocals: '#E8A849', drums: '#D4735E', bass: '#7B8F6A', other: '#6BA3B7', guitar: '#9B8EC4', piano: '#B07DA0' }
