from integrations.qiskit.qasm_exporter import export_qiskit_qasm
from qmodel.circuit.validators import CircuitValidator


def export_qasm(circuit_model):
    validator = CircuitValidator()
    validator.validate(circuit_model)

    return export_qiskit_qasm(circuit_model)