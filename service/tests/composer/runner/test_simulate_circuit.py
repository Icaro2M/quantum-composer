import pytest

from composer.runner.simulate_circuit import simulate_circuit
from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation
from qmodel.circuit.exceptions import InvalidGateError


def create_valid_measured_circuit_model():
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
    circuit.add_operation(
        QuantumOperation(
            id="op-2",
            gate="MEASURE",
            targets=[0],
            controls=[],
            parameters=[0],
            position=1,
        )
    )

    return circuit


def test_simulate_circuit_validates_and_delegates_to_qiskit_simulator(monkeypatch):
    circuit = create_valid_measured_circuit_model()
    expected_result = {
        "shots": 256,
        "counts": {"0": 128, "1": 128},
    }
    captured = {}

    def fake_simulate_qiskit_circuit(circuit_model, shots):
        captured["circuit_model"] = circuit_model
        captured["shots"] = shots
        return expected_result

    monkeypatch.setattr(
        "composer.runner.simulate_circuit.simulate_qiskit_circuit",
        fake_simulate_qiskit_circuit,
    )

    result = simulate_circuit(circuit, shots=256)

    assert result == expected_result
    assert captured == {
        "circuit_model": circuit,
        "shots": 256,
    }


def test_simulate_circuit_does_not_simulate_invalid_circuit(monkeypatch):
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

    def fake_simulate_qiskit_circuit(circuit_model, shots):
        raise AssertionError("simulator should not be called")

    monkeypatch.setattr(
        "composer.runner.simulate_circuit.simulate_qiskit_circuit",
        fake_simulate_qiskit_circuit,
    )

    with pytest.raises(InvalidGateError):
        simulate_circuit(circuit)
