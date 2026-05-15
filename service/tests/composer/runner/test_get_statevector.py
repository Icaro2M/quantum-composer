import pytest

from composer.runner.get_statevector import get_statevector
from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation
from qmodel.circuit.exceptions import InvalidGateError


def create_valid_circuit_model():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=0)
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


def test_get_statevector_validates_and_delegates_to_qiskit_simulator(monkeypatch):
    circuit = create_valid_circuit_model()
    expected_result = {
        "statevector": [
            {"real": 0.70710678118, "imag": 0.0},
            {"real": 0.70710678118, "imag": 0.0},
        ],
        "probabilities": {"0": 0.5, "1": 0.5},
    }
    captured = {}

    def fake_get_qiskit_statevector(circuit_model):
        captured["circuit_model"] = circuit_model
        return expected_result

    monkeypatch.setattr(
        "composer.runner.get_statevector.get_qiskit_statevector",
        fake_get_qiskit_statevector,
    )

    result = get_statevector(circuit)

    assert result == expected_result
    assert captured["circuit_model"] is circuit


def test_get_statevector_does_not_run_invalid_circuit(monkeypatch):
    circuit = QuantumCircuitModel(qubits=1, classical_bits=0)
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

    def fake_get_qiskit_statevector(circuit_model):
        raise AssertionError("statevector backend should not be called")

    monkeypatch.setattr(
        "composer.runner.get_statevector.get_qiskit_statevector",
        fake_get_qiskit_statevector,
    )

    with pytest.raises(InvalidGateError):
        get_statevector(circuit)
