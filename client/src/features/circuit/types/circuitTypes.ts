export type GateName =
  | 'H'
  | 'X'
  | 'Y'
  | 'Z'
  | 'CX'
  | 'RX'
  | 'RY'
  | 'RZ'
  | 'MEASURE'

export type CircuitOperation = {
  id: string
  gate: GateName
  targets: number[]
  controls: number[]
  parameters: number[]
  position: number
}

export type CircuitModel = {
  qubits: number
  classical_bits: number
  operations: CircuitOperation[]
}

export type GateDefinition = {
  name: GateName
  label: string
  description: string
  category: 'single' | 'controlled' | 'parametric' | 'measurement'
}

export type ValidationResult = {
  valid: boolean
  errors: string[]
}

export type SimulationResult = {
  shots: number
  counts: Record<string, number>
}

export type StatevectorResult = {
  statevector: Array<{
    real: number
    imag: number
  }>
  probabilities: Record<string, number>
}

export type QasmResult = {
  format: string
  qasm: string
}

export type TranspileResult = {
  optimization_level: number
  depth: number
  width: number
  size: number
  operations: Record<string, number>
  qasm: string
}

export type ApiErrorPayload = {
  error?: string
  message?: string
  detail?: string
}
