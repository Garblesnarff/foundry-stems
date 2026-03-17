import type { DragEvent } from 'react'
import { useState } from 'react'

export function useDropzone(onFiles: (files: File[]) => void) {
  const [dragOver, setDragOver] = useState(false)
  return {
    dragOver,
    onDragOver: (e: DragEvent) => {
      e.preventDefault()
      setDragOver(true)
    },
    onDragLeave: () => setDragOver(false),
    onDrop: (e: DragEvent) => {
      e.preventDefault()
      setDragOver(false)
      onFiles(Array.from(e.dataTransfer.files))
    },
  }
}
