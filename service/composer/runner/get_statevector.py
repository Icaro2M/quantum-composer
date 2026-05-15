from integrations.qiskit.simulator import get_qiskit_statevector
from qmodel.circuit.validators import CircuitValidator


def get_statevector(circuit_model):
    validator = CircuitValidator()
    validator.validate(circuit_model)

    return get_qiskit_statevector(circuit_model)