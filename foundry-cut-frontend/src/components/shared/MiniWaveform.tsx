export function MiniWaveform({ color, active = false }: { color: string; active?: boolean }) {
  return <div className="flex gap-[2px] h-10 items-end">{Array.from({ length: 28 }).map((_, i) => {
    const h = 8 + Math.sin(i * 0.3) * 8 + Math.cos(i * 0.7) * 6
    return <div key={i} className={`waveform-bar ${active ? 'active' : 'inactive'}`} style={{height: `${Math.max(4, h)}px`, backgroundColor: active ? color : undefined, animationDuration: `${1 + (i % 5) * 0.3}s`, animationDelay: `${i * 0.03}s`}} />
  })}</div>
}
