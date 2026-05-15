import pytest

from integrations.qiskit.simulator import (
    QiskitSimulator,
    get_qiskit_statevector,
    simulate_qiskit_circuit,
)
from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation


def create_single_qubit_h_measure_circuit():
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


def create_single_qubit_h_circuit():
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


def test_simulate_returns_counts_and_uses_requested_shots():
    result = simulate_qiskit_circuit(
        create_single_qubit_h_measure_circuit(),
        shots=64,
    )

    assert result["shots"] == 64
    assert sum(result["counts"].values()) == 64
    assert set(result["counts"]).issubset({"0", "1"})


def test_simulator_uses_default_shots_when_override_is_not_provided():
    simulator = QiskitSimulator(shots=32)

    result = simulator.simulate(create_single_qubit_h_measure_circuit())

    assert result["shots"] == 32
    assert sum(result["counts"].values()) == 32


def test_get_statevector_serializes_amplitudes_and_probabilities():
    result = get_qiskit_statevector(create_single_qubit_h_circuit())

    assert result["statevector"] == [
        {"real": pytest.approx(2**-0.5), "imag": 0.0},
        {"real": pytest.approx(2**-0.5), "imag": 0.0},
    ]
    assert result["probabilities"] == {
        "0": pytest.approx(0.5),
        "1": pytest.approx(0.5),
    }
