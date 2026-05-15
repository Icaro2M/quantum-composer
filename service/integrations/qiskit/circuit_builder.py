from qiskit import QuantumCircuit


class QiskitCircuitBuilder:
    def build(self, circuit_model):
        circuit = QuantumCircuit(
            circuit_model.get_qubit_count(),
            circuit_model.get_classical_bit_count(),
        )

        for operation in circuit_model.get_operations_ordered():
            self._apply_operation(circuit, operation)

        return circuit

    def _apply_operation(self, circuit, operation):
        gate = operation.gate.upper()

        if gate == "MEASURE":
            self._apply_measurement(circuit, operation)
            return

        if gate == "H":
            circuit.h(operation.targets[0])
            return

        if gate == "X":
            circuit.x(operation.targets[0])
            return

        if gate == "Y":
            circuit.y(operation.targets[0])
            return

        if gate == "Z":
            circuit.z(operation.targets[0])
            return

        if gate == "S":
            circuit.s(operation.targets[0])
            return

        if gate == "T":
            circuit.t(operation.targets[0])
            return

        if gate == "I":
            circuit.id(operation.targets[0])
            return

        if gate == "CX":
            circuit.cx(operation.controls[0], operation.targets[0])
            return

        if gate == "CZ":
            circuit.cz(operation.controls[0], operation.targets[0])
            return

        if gate == "CY":
            circuit.cy(operation.controls[0], operation.targets[0])
            return

        if gate == "CH":
            circuit.ch(operation.controls[0], operation.targets[0])
            return

        if gate == "SWAP":
            circuit.swap(operation.targets[0], operation.targets[1])
            return

        if gate == "CCX":
            circuit.ccx(
                operation.controls[0],
                operation.controls[1],
                operation.targets[0],
            )
            return

        if gate == "RX":
            circuit.rx(operation.parameters[0], operation.targets[0])
            return

        if gate == "RY":
            circuit.ry(operation.parameters[0], operation.targets[0])
            return

        if gate == "RZ":
            circuit.rz(operation.parameters[0], operation.targets[0])
            return

        if gate == "P":
            circuit.p(operation.parameters[0], operation.targets[0])
            return

        if gate == "U":
            circuit.u(
                operation.parameters[0],
                operation.parameters[1],
                operation.parameters[2],
                operation.targets[0],
            )
            return

        if gate == "CRX":
            circuit.crx(
                operation.parameters[0],
                operation.controls[0],
                operation.targets[0],
            )
            return

        if gate == "CRY":
            circuit.cry(
                operation.parameters[0],
                operation.controls[0],
                operation.targets[0],
            )
            return

        if gate == "CRZ":
            circuit.crz(
                operation.parameters[0],
                operation.controls[0],
                operation.targets[0],
            )
            return

        raise ValueError(f"Unsupported Qiskit gate: {operation.gate}")

    def _apply_measurement(self, circuit, operation):
        qubit_index = operation.targets[0]
        classical_bit_index = operation.parameters[0]

        circuit.measure(qubit_index, classical_bit_index)


def build_qiskit_circuit(circuit_model):
    return QiskitCircuitBuilder().build(circuit_model)