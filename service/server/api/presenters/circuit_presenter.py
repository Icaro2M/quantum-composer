from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation


def schema_to_circuit_model(circuit_schema):
    circuit_model = QuantumCircuitModel(
        qubits=circuit_schema.qubits,
        classical_bits=circuit_schema.classical_bits,
    )

    for operation_schema in circuit_schema.operations:
        operation = QuantumOperation(
            id=operation_schema.id,
            gate=operation_schema.gate,
            targets=operation_schema.targets,
            controls=operation_schema.controls,
            parameters=operation_schema.parameters,
            position=operation_schema.position,
        )

        circuit_model.add_operation(operation)

    return circuit_model