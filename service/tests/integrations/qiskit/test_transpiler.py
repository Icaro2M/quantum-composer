from integrations.qiskit.qasm_exporter import export_qiskit_qasm
from integrations.qiskit.transpiler import transpile_qiskit_circuit
from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation


def create_bell_circuit_model():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)
    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="H",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )
    circuit.add_operation(
        QuantumOperation(
            id="op-2",
            gate="CX",
            targets=[1],
            controls=[0],
            parameters=[],
            position=1,
        )
    )
    circuit.add_operation(
        QuantumOperation(
            id="op-3",
            gate="MEASURE",
            targets=[0],
            controls=[],
            parameters=[0],
            position=2,
        )
    )
    circuit.add_operation(
        QuantumOperation(
            id="op-4",
            gate="MEASURE",
            targets=[1],
            controls=[],
            parameters=[1],
            position=3,
        )
    )

    return circuit


def test_transpile_qiskit_circuit_returns_metadata_and_qasm():
    result = transpile_qiskit_circuit(
        create_bell_circuit_model(),
        optimization_level=2,
    )

    assert result["optimization_level"] == 2
    assert result["depth"] >= 1
    assert result["width"] == 4
    assert result["size"] >= 4
    assert result["operations"]["h"] == 1
    assert result["operations"]["cx"] == 1
    assert result["operations"]["measure"] == 2
    assert "OPENQASM 3" in result["qasm"]


def test_export_qiskit_qasm_returns_openqasm_3_payload():
    result = export_qiskit_qasm(create_bell_circuit_model())

    assert result["format"] == "OPENQASM 3.0"
    assert "OPENQASM 3" in result["qasm"]
    assert "h" in result["qasm"]
    assert "cx" in result["qasm"]
