import pytest

from composer.circuit.export_qasm import export_qasm
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


def test_export_qasm_validates_and_delegates_to_qiskit_exporter(monkeypatch):
    circuit = create_valid_circuit_model()
    expected_result = {
        "format": "OPENQASM 3.0",
        "qasm": "OPENQASM 3.0;",
    }
    captured = {}

    def fake_export_qiskit_qasm(circuit_model):
        captured["circuit_model"] = circuit_model
        return expected_result

    monkeypatch.setattr(
        "composer.circuit.export_qasm.export_qiskit_qasm",
        fake_export_qiskit_qasm,
    )

    result = export_qasm(circuit)

    assert result == expected_result
    assert captured["circuit_model"] is circuit


def test_export_qasm_does_not_export_invalid_circuit(monkeypatch):
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

    def fake_export_qiskit_qasm(circuit_model):
        raise AssertionError("exporter should not be called")

    monkeypatch.setattr(
        "composer.circuit.export_qasm.export_qiskit_qasm",
        fake_export_qiskit_qasm,
    )

    with pytest.raises(InvalidGateError):
        export_qasm(circuit)
