import { create } from 'zustand'
import type {
  CircuitModel,
  CircuitOperation,
  GateName,
} from '../types/circuitTypes'

type CircuitState = {
  qubits: number
  classicalBits: number
  columns: number
  operations: CircuitOperation[]
  selectedGate: GateName
  selectedParameter: number
  setSelectedGate: (gate: GateName) => void
  setSelectedParameter: (value: number) => void
  setQubits: (value: number) => void
  setClassicalBits: (value: number) => void
  setColumns: (value: number) => void
  placeGate: (position: number, qubit: number) => void
  removeOperation: (id: string) => void
  ensureMeasurementsAtEnd: () => void
  clearCircuit: () => void
  loadBellCircuit: () => void
  toCircuitModel: () => CircuitModel
}

function createOperation(
  gate: GateName,
  position: number,
  qubit: number,
  qubits: number,
  parameter: number,
): CircuitOperation {
  const id = `${gate}-${position}-${qubit}-${Date.now()}`

  if (gate === 'CX') {
    const control = qubit === 0 && qubits > 1 ? 1 : Math.max(0, qubit - 1)

    return {
      id,
      gate,
      targets: [qubit],
      controls: [control],
      parameters: [],
      position,
    }
  }

  if (gate === 'MEASURE') {
    return {
      id,
      gate,
      targets: [qubit],
      controls: [],
      parameters: [qubit],
      position,
    }
  }

  if (gate === 'RX' || gate === 'RY' || gate === 'RZ') {
    return {
      id,
      gate,
      targets: [qubit],
      controls: [],
      parameters: [parameter],
      position,
    }
  }

  return {
    id,
    gate,
    targets: [qubit],
    controls: [],
    parameters: [],
    position,
  }
}

export const useCircuitStore = create<CircuitState>((set, get) => ({
  qubits: 2,
  classicalBits: 2,
  columns: 8,
  operations: [
    {
      id: 'starter-h',
      gate: 'H',
      targets: [0],
      controls: [],
      parameters: [],
      position: 0,
    },
    {
      id: 'starter-cx',
      gate: 'CX',
      targets: [1],
      controls: [0],
      parameters: [],
      position: 1,
    },
    {
      id: 'starter-m0',
      gate: 'MEASURE',
      targets: [0],
      controls: [],
      parameters: [0],
      position: 2,
    },
    {
      id: 'starter-m1',
      gate: 'MEASURE',
      targets: [1],
      controls: [],
      parameters: [1],
      position: 3,
    },
  ],
  selectedGate: 'H',
  selectedParameter: 1.5708,
  setSelectedGate: (gate) => set({ selectedGate: gate }),
  setSelectedParameter: (value) => set({ selectedParameter: value }),
  setQubits: (value) =>
    set((state) => ({
      qubits: value,
      classicalBits: Math.max(state.classicalBits, value),
      operations: state.operations.filter((operation) =>
        operation.targets.every((target) => target < value),
      ),
    })),
  setClassicalBits: (value) => set({ classicalBits: value }),
  setColumns: (value) =>
    set((state) => ({
      columns: value,
      operations: state.operations.filter(
        (operation) => operation.position < value,
      ),
    })),
  placeGate: (position, qubit) =>
    set((state) => {
      const nextOperation = createOperation(
        state.selectedGate,
        position,
        qubit,
        state.qubits,
        state.selectedParameter,
      )

      const operations = state.operations.filter(
        (operation) =>
          !(operation.position === position && operation.targets.includes(qubit)),
      )

      return {
        operations: [...operations, nextOperation],
      }
    }),
  removeOperation: (id) =>
    set((state) => ({
      operations: state.operations.filter((operation) => operation.id !== id),
    })),
  ensureMeasurementsAtEnd: () =>
    set((state) => {
      const lastNonMeasurementPosition = state.operations
        .filter((operation) => operation.gate !== 'MEASURE')
        .reduce(
          (lastPosition, operation) => Math.max(lastPosition, operation.position),
          -1,
        )
      const measurementPosition = Math.max(
        state.columns - 1,
        lastNonMeasurementPosition + 1,
      )
      const measuredQubits = new Set(
        state.operations
          .filter((operation) => operation.gate === 'MEASURE')
          .flatMap((operation) => operation.targets),
      )
      const missingMeasurements = Array.from(
        { length: state.qubits },
        (_, qubit) => qubit,
      )
        .filter((qubit) => !measuredQubits.has(qubit))
        .map((qubit) => ({
          id: `auto-measure-${qubit}-${Date.now()}`,
          gate: 'MEASURE' as const,
          targets: [qubit],
          controls: [],
          parameters: [qubit],
          position: measurementPosition,
        }))

      return {
        columns: Math.max(state.columns, measurementPosition + 1),
        classicalBits: Math.max(state.classicalBits, state.qubits),
        operations: [...state.operations, ...missingMeasurements],
      }
    }),
  clearCircuit: () => set({ operations: [] }),
  loadBellCircuit: () =>
    set({
      qubits: 2,
      classicalBits: 2,
      columns: 8,
      operations: [
        {
          id: 'bell-h',
          gate: 'H',
          targets: [0],
          controls: [],
          parameters: [],
          position: 0,
        },
        {
          id: 'bell-cx',
          gate: 'CX',
          targets: [1],
          controls: [0],
          parameters: [],
          position: 1,
        },
        {
          id: 'bell-m0',
          gate: 'MEASURE',
          targets: [0],
          controls: [],
          parameters: [0],
          position: 2,
        },
        {
          id: 'bell-m1',
          gate: 'MEASURE',
          targets: [1],
          controls: [],
          parameters: [1],
          position: 3,
        },
      ],
    }),
  toCircuitModel: () => {
    const state = get()

    return {
      qubits: state.qubits,
      classical_bits: state.classicalBits,
      operations: state.operations
        .map((operation) => ({
          ...operation,
          parameters:
            operation.gate === 'MEASURE'
              ? [Math.min(operation.targets[0], state.classicalBits - 1)]
              : operation.parameters,
        }))
        .sort((left, right) => left.position - right.position),
    }
  },
}))
