from qiskit import qasm3

from integrations.qiskit.circuit_builder import build_qiskit_circuit


class QiskitQasmExporter:
    def export(self, circuit_model):
        qiskit_circuit = build_qiskit_circuit(circuit_model)

        return {
            "format": "OPENQASM 3.0",
            "qasm": qasm3.dumps(qiskit_circuit),
        }


def export_qiskit_qasm(circuit_model):
    return QiskitQasmExporter().export(circuit_model)