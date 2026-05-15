import pytest

from composer.circuit.transpile_circuit import transpile_circuit
from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation
from qmodel.circuit.exceptions import InvalidGateError


def create_valid_circuit_model():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)
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

    return circuit


def test_transpile_circuit_validates_and_delegates_to_qiskit_transpiler(monkeypatch):
    circuit = create_valid_circuit_model()
    expected_result = {
        "optimization_level": 2,
        "depth": 1,
        "width": 1,
        "size": 1,
        "operations": {"h": 1},
        "qasm": "OPENQASM 3.0;",
    }
    captured = {}

    def fake_transpile_qiskit_circuit(circuit_model, optimization_level):
        captured["circuit_model"] = circuit_model
        captured["optimization_level"] = optimization_level
        return expected_result

    monkeypatch.setattr(
        "composer.circuit.transpile_circuit.transpile_qiskit_circuit",
        fake_transpile_qiskit_circuit,
    )

    result = transpile_circuit(circuit, optimization_level=2)

    assert result == expected_result
    assert captured == {
        "circuit_model": circuit,
        "optimization_level": 2,
    }


def test_transpile_circuit_does_not_transpile_invalid_circuit(monkeypatch):
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)
    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="UNKNOWN",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    def fake_transpile_qiskit_circuit(circuit_model, optimization_level):
        raise AssertionError("transpiler should not be called")

    monkeypatch.setattr(
        "composer.circuit.transpile_circuit.transpile_qiskit_circuit",
        fake_transpile_qiskit_circuit,
    )

    with pytest.raises(InvalidGateError):
        transpile_circuit(circuit)
