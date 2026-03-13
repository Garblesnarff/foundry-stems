import { useRef, useState } from 'react'

export function useAudioPlayer() {
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [playing, setPlaying] = useState(false)

  const play = (src: string) => {
    if (!audioRef.current) audioRef.current = new Audio()
    audioRef.current.src = src
    void audioRef.current.play()
    setPlaying(true)
    audioRef.current.onended = () => setPlaying(false)
  }
  const pause = () => { audioRef.current?.pause(); setPlaying(false) }
  return { playing, play, pause }
}
