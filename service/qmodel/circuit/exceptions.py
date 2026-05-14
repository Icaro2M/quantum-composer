class CircuitError(Exception):
    """Base exception for circuit domain errors."""
    pass


class InvalidCircuitError(CircuitError):
    """Raised when the circuit structure is invalid."""
    pass


class InvalidOperationError(CircuitError):
    """Raised when an operation is invalid."""
    pass


class DuplicateOperationIdError(CircuitError):
    """Raised when an operation id already exists in the circuit."""

    def __init__(self, operation_id):
        self.operation_id = operation_id
        super().__init__(f"Operation id already exists: {operation_id}")


class OperationNotFoundError(CircuitError):
    """Raised when an operation cannot be found."""

    def __init__(self, operation_id):
        self.operation_id = operation_id
        super().__init__(f"Operation not found: {operation_id}")


class InvalidQubitIndexError(CircuitError):
    """Raised when a qubit index is outside the circuit range."""

    def __init__(self, qubit_index):
        self.qubit_index = qubit_index
        super().__init__(f"Invalid qubit index: {qubit_index}")


class InvalidClassicalBitIndexError(CircuitError):
    """Raised when a classical bit index is outside the circuit range."""

    def __init__(self, classical_bit_index):
        self.classical_bit_index = classical_bit_index
        super().__init__(f"Invalid classical bit index: {classical_bit_index}")


class InvalidGateError(CircuitError):
    """Raised when a gate is not supported by the circuit model."""

    def __init__(self, gate):
        self.gate = gate
        super().__init__(f"Invalid or unsupported gate: {gate}")


class InvalidGateArityError(CircuitError):
    """Raised when a gate receives an invalid number of targets, controls or parameters."""

    def __init__(self, gate, message=None):
        self.gate = gate
        detail = message or f"Invalid arity for gate: {gate}"
        super().__init__(detail)


class OperationConflictError(CircuitError):
    """Raised when two operations conflict at the same circuit position."""

    def __init__(self, position, qubits):
        self.position = position
        self.qubits = qubits
        super().__init__(
            f"Operation conflict at position {position} using qubits {qubits}"
        )


class InvalidMeasurementError(CircuitError):
    """Raised when a measurement operation is invalid."""
    pass


class InvalidParameterError(CircuitError):
    """Raised when an operation parameter is invalid."""

    def __init__(self, gate, parameter):
        self.gate = gate
        self.parameter = parameter
        super().__init__(f"Invalid parameter for gate {gate}: {parameter}")


class EmptyCircuitError(CircuitError):
    """Raised when an operation requires a non-empty circuit."""
    pass