import { useCircuitStore } from '../store/circuitStore'
import type { GateDefinition } from '../types/circuitTypes'
import { GateBlock } from './GateBlock'

const gates: GateDefinition[] = [
  {
    name: 'H',
    label: 'Hadamard',
    description: 'Cria superposicao',
    category: 'single',
  },
  {
    name: 'X',
    label: 'Pauli X',
    description: 'Inverte o qubit',
    category: 'single',
  },
  {
    name: 'Y',
    label: 'Pauli Y',
    description: 'Rotacao em Y',
    category: 'single',
  },
  {
    name: 'Z',
    label: 'Pauli Z',
    description: 'Inverte a fase',
    category: 'single',
  },
  {
    name: 'CX',
    label: 'Controlled X',
    description: 'Emaranha dois qubits',
    category: 'controlled',
  },
  {
    name: 'RX',
    label: 'Rotate X',
    description: 'Porta parametrica',
    category: 'parametric',
  },
  {
    name: 'RY',
    label: 'Rotate Y',
    description: 'Porta parametrica',
    category: 'parametric',
  },
  {
    name: 'RZ',
    label: 'Rotate Z',
    description: 'Porta parametrica',
    category: 'parametric',
  },
  {
    name: 'MEASURE',
    label: 'Measure',
    description: 'Mede em bit classico',
    category: 'measurement',
  },
]

export function GatePalette() {
  const selectedGate = useCircuitStore((state) => state.selectedGate)
  const selectedParameter = useCircuitStore((state) => state.selectedParameter)
  const setSelectedGate = useCircuitStore((state) => state.setSelectedGate)
  const setSelectedParameter = useCircuitStore(
    (state) => state.setSelectedParameter,
  )
  const loadBellCircuit = useCircuitStore((state) => state.loadBellCircuit)
  const clearCircuit = useCircuitStore((state) => state.clearCircuit)
  const ensureMeasurementsAtEnd = useCircuitStore(
    (state) => state.ensureMeasurementsAtEnd,
  )

  return (
    <aside className="gate-palette" aria-label="Paleta de portas">
      <div className="panel-heading">
        <p className="eyebrow">Portas</p>
        <h2>Montagem</h2>
      </div>

      <div className="gate-list">
        {gates.map((gate) => (
          <button
            key={gate.name}
            type="button"
            className={
              selectedGate === gate.name ? 'gate-option is-selected' : 'gate-option'
            }
            onClick={() => setSelectedGate(gate.name)}
          >
            <GateBlock gate={gate.name} muted={selectedGate !== gate.name} />
            <span>
              <strong>{gate.label}</strong>
              <small>{gate.description}</small>
            </span>
          </button>
        ))}
      </div>

      <label className="field">
        <span>Parametro de rotacao</span>
        <input
          type="number"
          step="0.01"
          value={selectedParameter}
          onChange={(event) => setSelectedParameter(Number(event.target.value))}
        />
      </label>

      <div className="palette-actions">
        <button type="button" className="secondary-button" onClick={loadBellCircuit}>
          Bell
        </button>
        <button
          type="button"
          className="secondary-button"
          onClick={ensureMeasurementsAtEnd}
        >
          Medir todos
        </button>
        <button type="button" className="ghost-button" onClick={clearCircuit}>
          Limpar
        </button>
      </div>
    </aside>
  )
}
