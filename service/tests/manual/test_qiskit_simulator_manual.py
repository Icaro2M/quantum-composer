from qmodel.circuit.entities import QuantumCircuitModel, QuantumOperation

from composer.runner.simulate_circuit import simulate_circuit
from composer.runner.get_statevector import get_statevector
from composer.circuit.export_qasm import export_qasm
from composer.circuit.transpile_circuit import transpile_circuit
from composer.circuit.validate_circuit import validate_circuit


def create_bell_circuit_model():
    circuit_model = QuantumCircuitModel(qubits=2, classical_bits=2)

    circuit_model.add_operation(
        QuantumOperation(
            id="op1",
            gate="H",
            targets=[0],
            controls=[],
            parameters=[],
            position=0,
        )
    )

    circuit_model.add_operation(
        QuantumOperation(
            id="op2",
            gate="CX",
            targets=[1],
            controls=[0],
            parameters=[],
            position=1,
        )
    )

    circuit_model.add_operation(
        QuantumOperation(
            id="op3",
            gate="MEASURE",
            targets=[0],
            controls=[],
            parameters=[0],
            position=2,
        )
    )

    circuit_model.add_operation(
        QuantumOperation(
            id="op4",
            gate="MEASURE",
            targets=[1],
            controls=[],
            parameters=[1],
            position=3,
        )
    )

    return circuit_model


def main():
    circuit_model = create_bell_circuit_model()

    validation_result = validate_circuit(circuit_model)

    print("=== Validation result ===")
    print(validation_result)

    simulation_result = simulate_circuit(circuit_model, shots=1024)

    print()
    print("=== Simulation result ===")
    print(simulation_result)

    statevector_result = get_statevector(circuit_model)

    print()
    print("=== Statevector result ===")
    print(statevector_result)

    qasm_result = export_qasm(circuit_model)

    print()
    print("=== QASM result ===")
    print(qasm_result["format"])
    print(qasm_result["qasm"])

    transpile_result = transpile_circuit(
        circuit_model,
        optimization_level=1,
    )

    print()
    print("=== Transpile result ===")
    print("optimization_level:", transpile_result["optimization_level"])
    print("depth:", transpile_result["depth"])
    print("width:", transpile_result["width"])
    print("size:", transpile_result["size"])
    print("operations:", transpile_result["operations"])
    print()
    print(transpile_result["qasm"])


if __name__ == "__main__":
    main()