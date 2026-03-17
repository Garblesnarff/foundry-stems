export function EmberParticles() {
  return <div className="absolute inset-0 pointer-events-none overflow-hidden">{Array.from({length:12}).map((_,i)=><span key={i} className="absolute w-1.5 h-1.5 rounded-full bg-[var(--accent-amber)] opacity-70" style={{left:`${8+i*8}%`,bottom:0,animation:`ember ${2 + (i%4)}s linear infinite`,animationDelay:`${i*0.2}s`}} />)}</div>
}
