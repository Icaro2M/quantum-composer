import pytest

from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation
from qmodel.circuit.exceptions import (
    EmptyCircuitError,
    InvalidClassicalBitIndexError,
    InvalidGateArityError,
    InvalidGateError,
    InvalidMeasurementError,
    InvalidOperationError,
    InvalidParameterError,
    InvalidQubitIndexError,
    OperationConflictError,
)
from qmodel.circuit.validators import CircuitValidator


def test_valid_bell_circuit_passes_validation():
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
            position=2,
        )
    )

    validator = CircuitValidator()

    validator.validate(circuit)


def test_circuit_with_zero_qubits_raises_error():
    circuit = QuantumCircuitModel(qubits=0, classical_bits=1)
    validator = CircuitValidator()

    with pytest.raises(EmptyCircuitError):
        validator.validate(circuit)


def test_circuit_with_negative_classical_bits_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=-1)
    validator = CircuitValidator()

    with pytest.raises(InvalidClassicalBitIndexError):
        validator.validate(circuit)


def test_operation_with_empty_id_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="",
            gate="H",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidOperationError):
        validator.validate(circuit)


def test_operation_with_empty_gate_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidOperationError):
        validator.validate(circuit)


def test_invalid_gate_raises_error():
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

    validator = CircuitValidator()

    with pytest.raises(InvalidGateError):
        validator.validate(circuit)


def test_invalid_qubit_index_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="H",
            targets=[2],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidQubitIndexError):
        validator.validate(circuit)


def test_negative_qubit_index_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="H",
            targets=[-1],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidQubitIndexError):
        validator.validate(circuit)


def test_non_integer_qubit_index_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="H",
            targets=["0"],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidQubitIndexError):
        validator.validate(circuit)


def test_cx_without_control_raises_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="CX",
            targets=[1],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidGateArityError):
        validator.validate(circuit)


def test_cx_with_same_control_and_target_raises_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="CX",
            targets=[0],
            controls=[0],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidOperationError):
        validator.validate(circuit)


def test_rx_without_parameter_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="RX",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidGateArityError):
        validator.validate(circuit)


def test_rx_with_non_numeric_parameter_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="RX",
            targets=[0],
            controls=[],
            parameters=["pi"],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidParameterError):
        validator.validate(circuit)


def test_negative_position_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="H",
            targets=[0],
            controls=[],
            parameters=[],
            position=-1,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidOperationError):
        validator.validate(circuit)


def test_operation_conflict_same_position_and_same_qubit_raises_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=1)

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
            gate="X",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(OperationConflictError):
        validator.validate(circuit)


def test_operations_same_position_different_qubits_pass_validation():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=1)

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
            gate="X",
            targets=[1],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    validator.validate(circuit)


def test_valid_measurement_passes_validation():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="MEASURE",
            targets=[0],
            controls=[],
            parameters=[0],
            position=0,
        )
    )

    validator = CircuitValidator()

    validator.validate(circuit)


def test_measurement_without_classical_bit_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="MEASURE",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidMeasurementError):
        validator.validate(circuit)


def test_measurement_with_invalid_classical_bit_raises_error():
    circuit = QuantumCircuitModel(qubits=1, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="MEASURE",
            targets=[0],
            controls=[],
            parameters=[3],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidClassicalBitIndexError):
        validator.validate(circuit)


def test_measurement_with_control_raises_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="MEASURE",
            targets=[0],
            controls=[1],
            parameters=[0],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidMeasurementError):
        validator.validate(circuit)


def test_duplicated_targets_raise_error():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="SWAP",
            targets=[0, 0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidOperationError):
        validator.validate(circuit)


def test_duplicated_controls_raise_error():
    circuit = QuantumCircuitModel(qubits=3, classical_bits=1)

    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="CCX",
            targets=[2],
            controls=[0, 0],
            parameters=[],
            position=0,
        )
    )

    validator = CircuitValidator()

    with pytest.raises(InvalidOperationError):
        validator.validate(circuit)