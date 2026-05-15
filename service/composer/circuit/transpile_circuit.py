from integrations.qiskit.transpiler import transpile_qiskit_circuit
from qmodel.circuit.validators import CircuitValidator


def transpile_circuit(circuit_model, optimization_level=1):
    validator = CircuitValidator()
    validator.validate(circuit_model)

    return transpile_qiskit_circuit(
        circuit_model,
        optimization_level=optimization_level,
    )