import { isAxiosError } from 'axios'
import { useMemo, useState } from 'react'
import {
  exportQasm,
  getStatevector,
  simulateCircuit,
  transpileCircuit,
  validateCircuit,
} from '../services/circuitApi'
import { useCircuitStore } from '../store/circuitStore'
import type {
  ApiErrorPayload,
  QasmResult,
  SimulationResult,
  StatevectorResult,
  TranspileResult,
  ValidationResult,
} from '../types/circuitTypes'

type ResultState = {
  validation?: ValidationResult
  simulation?: SimulationResult
  statevector?: StatevectorResult
  qasm?: QasmResult
  transpile?: TranspileResult
}

function getErrorMessage(error: unknown) {
  if (isAxiosError<ApiErrorPayload>(error)) {
    const data = error.response?.data

    return data?.message ?? data?.detail ?? error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'Nao foi possivel concluir a chamada.'
}

export function SimulationPanel() {
  const toCircuitModel = useCircuitStore((state) => state.toCircuitModel)
  const ensureMeasurementsAtEnd = useCircuitStore(
    (state) => state.ensureMeasurementsAtEnd,
  )
  const operations = useCircuitStore((state) => state.operations)
  const [shots, setShots] = useState(1024)
  const [optimizationLevel, setOptimizationLevel] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState('Pronto para chamar a API.')
  const [results, setResults] = useState<ResultState>({})

  const orderedOperations = useMemo(
    () => [...operations].sort((left, right) => left.position - right.position),
    [operations],
  )

  async function runAction(action: () => Promise<void>) {
    setIsLoading(true)
    setStatus('Chamando o backend...')

    try {
      await action()
    } catch (error) {
      setStatus(getErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <aside className="simulation-panel" aria-label="Painel de simulacao">
      <div className="panel-heading">
        <p className="eyebrow">Backend</p>
        <h2>Execucao</h2>
      </div>

      <div className="run-controls">
        <label className="field">
          <span>Shots</span>
          <input
            type="number"
            min="1"
            max="100000"
            value={shots}
            onChange={(event) => setShots(Number(event.target.value))}
          />
        </label>
        <label className="field">
          <span>Otimizacao</span>
          <select
            value={optimizationLevel}
            onChange={(event) => setOptimizationLevel(Number(event.target.value))}
          >
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
          </select>
        </label>
      </div>

      <div className="action-grid">
        <button
          type="button"
          className="primary-button"
          disabled={isLoading}
          onClick={() =>
            runAction(async () => {
              const validation = await validateCircuit(toCircuitModel())
              setResults((current) => ({ ...current, validation }))
              setStatus('Circuito validado com sucesso.')
            })
          }
        >
          Validar
        </button>
        <button
          type="button"
          className="primary-button"
          disabled={isLoading}
          onClick={() =>
            runAction(async () => {
              ensureMeasurementsAtEnd()
              const simulation = await simulateCircuit(toCircuitModel(), shots)
              setResults((current) => ({ ...current, simulation }))
              setStatus('Simulacao concluida.')
            })
          }
        >
          Executar
        </button>
        <button
          type="button"
          className="secondary-button"
          disabled={isLoading}
          onClick={() =>
            runAction(async () => {
              const statevector = await getStatevector(toCircuitModel())
              setResults((current) => ({ ...current, statevector }))
              setStatus('Statevector calculado.')
            })
          }
        >
          Statevector
        </button>
        <button
          type="button"
          className="secondary-button"
          disabled={isLoading}
          onClick={() =>
            runAction(async () => {
              const qasm = await exportQasm(toCircuitModel())
              setResults((current) => ({ ...current, qasm }))
              setStatus('QASM exportado.')
            })
          }
        >
          QASM
        </button>
        <button
          type="button"
          className="secondary-button wide-button"
          disabled={isLoading}
          onClick={() =>
            runAction(async () => {
              const transpile = await transpileCircuit(
                toCircuitModel(),
                optimizationLevel,
              )
              setResults((current) => ({ ...current, transpile }))
              setStatus('Circuito transpilado.')
            })
          }
        >
          Transpilar
        </button>
      </div>

      <div className="status-line">{status}</div>

      <div className="summary-strip">
        <span>{orderedOperations.length} operacoes</span>
        <span>{toCircuitModel().qubits} qubits</span>
        <span>{toCircuitModel().classical_bits} bits</span>
      </div>

      <div className="results-panel">
        {results.simulation ? (
          <section>
            <h3>Contagens</h3>
            <div className="counts-list">
              {Object.entries(results.simulation.counts).map(([state, count]) => (
                <div key={state} className="count-row">
                  <span>{state}</span>
                  <strong>{count}</strong>
                </div>
              ))}
            </div>
          </section>
        ) : null}

        {results.statevector ? (
          <section>
            <h3>Probabilidades</h3>
            <div className="counts-list">
              {Object.entries(results.statevector.probabilities).map(
                ([state, probability]) => (
                  <div key={state} className="count-row">
                    <span>{state}</span>
                    <strong>{(probability * 100).toFixed(1)}%</strong>
                  </div>
                ),
              )}
            </div>
          </section>
        ) : null}

        {results.transpile ? (
          <section>
            <h3>Transpilacao</h3>
            <div className="metric-grid">
              <span>Depth {results.transpile.depth}</span>
              <span>Width {results.transpile.width}</span>
              <span>Size {results.transpile.size}</span>
            </div>
          </section>
        ) : null}

        {results.qasm ? (
          <section>
            <h3>{results.qasm.format}</h3>
            <pre>{results.qasm.qasm}</pre>
          </section>
        ) : null}
      </div>
    </aside>
  )
}
