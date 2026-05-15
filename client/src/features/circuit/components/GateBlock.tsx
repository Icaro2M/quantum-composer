import type { CircuitOperation, GateName } from '../types/circuitTypes'

type GateBlockProps = {
  gate?: GateName
  operation?: CircuitOperation
  muted?: boolean
  onClick?: () => void
}

export function GateBlock({ gate, operation, muted = false, onClick }: GateBlockProps) {
  const label = operation?.gate ?? gate ?? ''
  const className = [
    'gate-block',
    `gate-${label.toLowerCase()}`,
    muted ? 'is-muted' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <button
      type="button"
      className={className}
      onClick={onClick}
      title={operation ? 'Remover porta' : `Selecionar ${label}`}
    >
      <span>{label}</span>
    </button>
  )
}
