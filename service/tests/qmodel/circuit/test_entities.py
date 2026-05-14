import pytest

from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation
from qmodel.circuit.exceptions import (
    DuplicateOperationIdError,
    OperationNotFoundError,
)


def test_create_quantum_circuit_model():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    assert circuit.get_qubit_count() == 2
    assert circuit.get_classical_bit_count() == 2
    assert circuit.get_operations() == []


def test_add_operation():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation = QuantumOperation(
        id="op-1",
        gate="H",
        targets=[0],
        controls=[],
        parameters=[],
        position=0,
    )

    circuit.add_operation(operation)

    assert circuit.has_operation("op-1")
    assert circuit.get_operation("op-1") == operation
    assert len(circuit.get_operations()) == 1


def test_add_operation_with_duplicate_id_raises_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation_1 = QuantumOperation(
        id="op-1",
        gate="H",
        targets=[0],
        controls=[],
        parameters=[],
        position=0,
    )

    operation_2 = QuantumOperation(
        id="op-1",
        gate="X",
        targets=[1],
        controls=[],
        parameters=[],
        position=1,
    )

    circuit.add_operation(operation_1)

    with pytest.raises(DuplicateOperationIdError):
        circuit.add_operation(operation_2)


def test_remove_operation():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation = QuantumOperation(
        id="op-1",
        gate="H",
        targets=[0],
        controls=[],
        parameters=[],
        position=0,
    )

    circuit.add_operation(operation)
    circuit.remove_operation("op-1")

    assert not circuit.has_operation("op-1")
    assert len(circuit.get_operations()) == 0


def test_remove_missing_operation_raises_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    with pytest.raises(OperationNotFoundError):
        circuit.remove_operation("missing-op")


def test_get_operation_returns_none_when_not_found():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation = circuit.get_operation("missing-op")

    assert operation is None


def test_get_operations_ordered_by_position():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation_1 = QuantumOperation(
        id="op-1",
        gate="CX",
        targets=[1],
        controls=[0],
        parameters=[],
        position=2,
    )

    operation_2 = QuantumOperation(
        id="op-2",
        gate="H",
        targets=[0],
        controls=[],
        parameters=[],
        position=0,
    )

    operation_3 = QuantumOperation(
        id="op-3",
        gate="MEASURE",
        targets=[0],
        controls=[],
        parameters=[0],
        position=3,
    )

    circuit.add_operation(operation_1)
    circuit.add_operation(operation_2)
    circuit.add_operation(operation_3)

    ordered_operations = circuit.get_operations_ordered()

    assert ordered_operations[0].id == "op-2"
    assert ordered_operations[1].id == "op-1"
    assert ordered_operations[2].id == "op-3"


def test_get_operations_returns_copy():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation = QuantumOperation(
        id="op-1",
        gate="H",
        targets=[0],
        controls=[],
        parameters=[],
        position=0,
    )

    circuit.add_operation(operation)

    operations = circuit.get_operations()
    operations.clear()

    assert len(circuit.get_operations()) == 1


def test_clear_operations():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)

    operation = QuantumOperation(
        id="op-1",
        gate="H",
        targets=[0],
        controls=[],
        parameters=[],
        position=0,
    )

    circuit.add_operation(operation)
    circuit.clear_operations()

    assert circuit.get_operations() == []