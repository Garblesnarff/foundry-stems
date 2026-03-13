import { useRef } from 'react'
import { useDropzone } from '../../hooks/useDropzone'

export function Dropzone({ onFiles }: { onFiles: (files: File[]) => void }) {
  const inputRef = useRef<HTMLInputElement>(null)
  const dz = useDropzone(onFiles)
  return <div className={`dropzone ${dz.dragOver ? 'drag-over' : ''}`} onDragOver={dz.onDragOver} onDragLeave={dz.onDragLeave} onDrop={dz.onDrop} onClick={()=>inputRef.current?.click()}><div className="text-3xl mb-3">⚒️</div><div className="text-[16px] text-[var(--text-secondary)]">Drop your track into the forge</div><div className="mono text-[11px] text-[var(--text-dim)] mt-2">MP3, WAV, FLAC, OGG, M4A, AAC</div><input ref={inputRef} type="file" hidden onChange={(e)=>e.target.files && onFiles(Array.from(e.target.files))} /></div>
}
