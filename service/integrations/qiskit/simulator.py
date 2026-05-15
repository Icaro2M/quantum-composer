from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from integrations.qiskit.circuit_builder import build_qiskit_circuit


class QiskitSimulator:
    def __init__(self, shots=1024):
        self.shots = shots
        self.backend = AerSimulator()

    def simulate(self, circuit_model, shots=None):
        qiskit_circuit = build_qiskit_circuit(circuit_model)

        execution_shots = shots if shots is not None else self.shots

        job = self.backend.run(qiskit_circuit, shots=execution_shots)
        result = job.result()

        counts = result.get_counts(qiskit_circuit)

        return {
            "shots": execution_shots,
            "counts": counts,
        }

    def get_statevector(self, circuit_model):
        qiskit_circuit = build_qiskit_circuit(circuit_model)

        circuit_without_measurements = qiskit_circuit.remove_final_measurements(
            inplace=False
        )

        statevector = Statevector.from_instruction(circuit_without_measurements)

        return {
            "statevector": self._serialize_statevector(statevector),
            "probabilities": statevector.probabilities_dict(),
        }

    def _serialize_statevector(self, statevector):
        serialized = []

        for amplitude in statevector.data:
            serialized.append(
                {
                    "real": float(amplitude.real),
                    "imag": float(amplitude.imag),
                }
            )

        return serialized


def simulate_qiskit_circuit(circuit_model, shots=1024):
    return QiskitSimulator(shots=shots).simulate(circuit_model, shots=shots)


def get_qiskit_statevector(circuit_model):
    return QiskitSimulator().get_statevector(circuit_model)