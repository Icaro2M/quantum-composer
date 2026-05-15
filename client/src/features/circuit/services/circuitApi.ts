import { apiClient } from '../../../api/apiClient'
import type {
  CircuitModel,
  QasmResult,
  SimulationResult,
  StatevectorResult,
  TranspileResult,
  ValidationResult,
} from '../types/circuitTypes'

export async function validateCircuit(circuit: CircuitModel) {
  const response = await apiClient.post<ValidationResult>('/circuit/validate', {
    circuit,
  })

  return response.data
}

export async function exportQasm(circuit: CircuitModel) {
  const response = await apiClient.post<QasmResult>('/circuit/qasm', {
    circuit,
  })

  return response.data
}

export async function transpileCircuit(
  circuit: CircuitModel,
  optimizationLevel: number,
) {
  const response = await apiClient.post<TranspileResult>('/circuit/transpile', {
    circuit,
    optimization_level: optimizationLevel,
  })

  return response.data
}

export async function simulateCircuit(circuit: CircuitModel, shots: number) {
  const response = await apiClient.post<SimulationResult>('/simulation/run', {
    circuit,
    shots,
  })

  return response.data
}

export async function getStatevector(circuit: CircuitModel) {
  const response = await apiClient.post<StatevectorResult>(
    '/simulation/statevector',
    {
      circuit,
    },
  )

  return response.data
}
