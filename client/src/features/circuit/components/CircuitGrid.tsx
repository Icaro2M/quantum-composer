import { useCircuitStore } from '../store/circuitStore'
import type { CircuitOperation } from '../types/circuitTypes'
import { GateBlock } from './GateBlock'

function getOperationForCell(
  operations: CircuitOperation[],
  position: number,
  qubit: number,
) {
  return operations.find(
    (operation) =>
      operation.position === position && operation.targets.includes(qubit),
  )
}

function hasControlAtCell(
  operations: CircuitOperation[],
  position: number,
  qubit: number,
) {
  return operations.some(
    (operation) =>
      operation.position === position && operation.controls.includes(qubit),
  )
}

export function CircuitGrid() {
  const qubits = useCircuitStore((state) => state.qubits)
  const classicalBits = useCircuitStore((state) => state.classicalBits)
  const columns = useCircuitStore((state) => state.columns)
  const operations = useCircuitStore((state) => state.operations)
  const setQubits = useCircuitStore((state) => state.setQubits)
  const setClassicalBits = useCircuitStore((state) => state.setClassicalBits)
  const setColumns = useCircuitStore((state) => state.setColumns)
  const placeGate = useCircuitStore((state) => state.placeGate)
  const removeOperation = useCircuitStore((state) => state.removeOperation)

  const rows = Array.from({ length: qubits }, (_, index) => index)
  const positions = Array.from({ length: columns }, (_, index) => index)

  return (
    <section className="circuit-workbench" aria-label="Grade do circuito">
      <div className="workbench-toolbar">
        <div>
          <p className="eyebrow">Circuito</p>
          <h1>Quantum Composer</h1>
        </div>

        <div className="toolbar-fields">
          <label className="compact-field">
            <span>Qubits</span>
            <input
              type="number"
              min="1"
              max="5"
              value={qubits}
              onChange={(event) => setQubits(Number(event.target.value))}
            />
          </label>
          <label className="compact-field">
            <span>Bits</span>
            <input
              type="number"
              min="0"
              max="5"
              value={classicalBits}
              onChange={(event) => setClassicalBits(Number(event.target.value))}
            />
          </label>
          <label className="compact-field">
            <span>Colunas</span>
            <input
              type="number"
              min="4"
              max="12"
              value={columns}
              onChange={(event) => setColumns(Number(event.target.value))}
            />
          </label>
        </div>
      </div>

      <div
        className="circuit-grid"
        style={{
          gridTemplateColumns: `72px repeat(${columns}, minmax(58px, 1fr))`,
        }}
      >
        <div className="grid-corner" />
        {positions.map((position) => (
          <div key={`position-${position}`} className="position-label">
            {position}
          </div>
        ))}

        {rows.map((qubit) => (
          <div className="grid-row-fragment" key={`row-${qubit}`}>
            <div className="qubit-label">q[{qubit}]</div>
            {positions.map((position) => {
              const operation = getOperationForCell(operations, position, qubit)
              const isControl = hasControlAtCell(operations, position, qubit)

              return (
                <button
                  key={`${qubit}-${position}`}
                  type="button"
                  className={isControl ? 'grid-cell has-control' : 'grid-cell'}
                  onClick={() =>
                    operation
                      ? removeOperation(operation.id)
                      : placeGate(position, qubit)
                  }
                >
                  <span className="wire" />
                  {isControl ? <span className="control-dot" /> : null}
                  {operation ? <GateBlock operation={operation} /> : null}
                </button>
              )
            })}
          </div>
        ))}
      </div>

      <div className="circuit-note">
        Clique em uma porta da paleta e depois em uma celula. Clique em uma porta
        na grade para remover.
      </div>
    </section>
  )
}
