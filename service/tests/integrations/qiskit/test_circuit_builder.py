import pytest

from integrations.qiskit.circuit_builder import QiskitCircuitBuilder, build_qiskit_circuit
from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation


def create_bell_circuit_model():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=2)
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


def test_build_qiskit_circuit_applies_operations_in_position_order():
    qiskit_circuit = build_qiskit_circuit(create_bell_circuit_model())

    assert qiskit_circuit.num_qubits == 2
    assert qiskit_circuit.num_clbits == 2
    assert [instruction.operation.name for instruction in qiskit_circuit.data] == [
        "h",
        "cx",
        "measure",
        "measure",
    ]


def test_builder_applies_parametric_and_controlled_parametric_gates():
    circuit = QuantumCircuitModel(qubits=2, classical_bits=0)
    circuit.add_operation(
        QuantumOperation(
            id="op-1",
            gate="RX",
            targets=[0],
            controls=[],
            parameters=[0.5],
            position=0,
        )
    )
    circuit.add_operation(
        QuantumOperation(
            id="op-2",
            gate="CRZ",
            targets=[1],
            controls=[0],
            parameters=[1.25],
            position=1,
        )
    )

    qiskit_circuit = QiskitCircuitBuilder().build(circuit)

    assert [instruction.operation.name for instruction in qiskit_circuit.data] == [
        "rx",
        "crz",
    ]
    assert float(qiskit_circuit.data[0].operation.params[0]) == pytest.approx(0.5)
    assert float(qiskit_circuit.data[1].operation.params[0]) == pytest.approx(1.25)


def test_builder_raises_for_unsupported_gate():
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

    with pytest.raises(ValueError, match="Unsupported Qiskit gate"):
        build_qiskit_circuit(circuit)
