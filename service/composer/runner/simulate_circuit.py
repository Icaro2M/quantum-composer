from integrations.qiskit.simulator import simulate_qiskit_circuit
from qmodel.circuit.validators import CircuitValidator


def simulate_circuit(circuit_model, shots=1024):
    validator = CircuitValidator()
    validator.validate(circuit_model)

    return simulate_qiskit_circuit(
        circuit_model,
        shots=shots,
    )