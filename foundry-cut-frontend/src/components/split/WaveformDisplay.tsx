import { MiniWaveform } from '../shared/MiniWaveform'

export function WaveformDisplay({ color, active }: { color: string; active?: boolean }) { return <MiniWaveform color={color} active={active} /> }
