from qiskit import transpile

from integrations.qiskit.circuit_builder import build_qiskit_circuit


class QiskitTranspiler:
    def transpile(self, circuit_model, optimization_level=1):
        qiskit_circuit = build_qiskit_circuit(circuit_model)

        transpiled_circuit = transpile(
            qiskit_circuit,
            optimization_level=optimization_level,
        )

        return {
            "optimization_level": optimization_level,
            "depth": transpiled_circuit.depth(),
            "width": transpiled_circuit.width(),
            "size": transpiled_circuit.size(),
            "operations": dict(transpiled_circuit.count_ops()),
            "qasm": self._to_qasm(transpiled_circuit),
        }

    def _to_qasm(self, qiskit_circuit):
        from qiskit import qasm3

        return qasm3.dumps(qiskit_circuit)


def transpile_qiskit_circuit(circuit_model, optimization_level=1):
    return QiskitTranspiler().transpile(
        circuit_model,
        optimization_level=optimization_level,
    )