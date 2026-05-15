from qmodel.circuit.validators import CircuitValidator


def validate_circuit(circuit_model):
    validator = CircuitValidator()
    validator.validate(circuit_model)

    return {
        "valid": True,
        "errors": [],
    }