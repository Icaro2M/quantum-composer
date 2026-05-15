import pytest

from composer.circuit.validate_circuit import validate_circuit
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


def test_validate_circuit_returns_success_result_for_valid_circuit():
    result = validate_circuit(create_valid_circuit_model())

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_circuit_raises_domain_error_for_invalid_circuit():
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

    with pytest.raises(InvalidGateError):
        validate_circuit(circuit)
