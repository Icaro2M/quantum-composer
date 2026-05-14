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
from qmodel.circuit.gates import get_gate_definition, is_supported_gate


class CircuitValidator:

    def validate(self, circuit):
        self.validate_circuit_structure(circuit)
        self.validate_operations(circuit)
        self.validate_operation_conflicts(circuit)

    def validate_circuit_structure(self, circuit):
        if circuit.qubits <= 0:
            raise EmptyCircuitError()

        if circuit.classical_bits < 0:
            raise InvalidClassicalBitIndexError(circuit.classical_bits)

    def validate_operations(self, circuit):
        for operation in circuit.get_operations():
            self.validate_operation(circuit, operation)

    def validate_operation(self, circuit, operation):
        self.validate_operation_base(operation)

        if operation.gate == "MEASURE":
            self.validate_measurement_operation(circuit, operation)
            return

        self.validate_gate_exists(operation)
        self.validate_gate_arity(operation)
        self.validate_qubit_indexes(circuit, operation)
        self.validate_parameters(operation)

    def validate_operation_base(self, operation):
        if operation.id is None or operation.id == "":
            raise InvalidOperationError("Operation id cannot be empty.")

        if operation.gate is None or operation.gate == "":
            raise InvalidOperationError("Operation gate cannot be empty.")

        if operation.targets is None:
            raise InvalidOperationError("Operation targets cannot be None.")

        if operation.controls is None:
            raise InvalidOperationError("Operation controls cannot be None.")

        if operation.parameters is None:
            raise InvalidOperationError("Operation parameters cannot be None.")

        if operation.position is None:
            raise InvalidOperationError("Operation position cannot be None.")

        if operation.position < 0:
            raise InvalidOperationError("Operation position cannot be negative.")

    def validate_gate_exists(self, operation):
        if not is_supported_gate(operation.gate):
            raise InvalidGateError(operation.gate)

    def validate_gate_arity(self, operation):
        gate_definition = get_gate_definition(operation.gate)

        if len(operation.targets) != gate_definition.target_count:
            raise InvalidGateArityError(
                operation.gate,
                f"Gate {operation.gate} expects {gate_definition.target_count} target(s), "
                f"but received {len(operation.targets)}.",
            )

        if len(operation.controls) != gate_definition.control_count:
            raise InvalidGateArityError(
                operation.gate,
                f"Gate {operation.gate} expects {gate_definition.control_count} control(s), "
                f"but received {len(operation.controls)}.",
            )

        if len(operation.parameters) != gate_definition.parameter_count:
            raise InvalidGateArityError(
                operation.gate,
                f"Gate {operation.gate} expects {gate_definition.parameter_count} parameter(s), "
                f"but received {len(operation.parameters)}.",
            )

    def validate_qubit_indexes(self, circuit, operation):
        used_qubits = operation.targets + operation.controls

        for qubit_index in used_qubits:
            if not isinstance(qubit_index, int):
                raise InvalidQubitIndexError(qubit_index)

            if qubit_index < 0 or qubit_index >= circuit.qubits:
                raise InvalidQubitIndexError(qubit_index)

        for target in operation.targets:
            if target in operation.controls:
                raise InvalidOperationError(
                    f"Qubit {target} cannot be both target and control."
                )

        if len(set(operation.targets)) != len(operation.targets):
            raise InvalidOperationError("Operation cannot have duplicated targets.")

        if len(set(operation.controls)) != len(operation.controls):
            raise InvalidOperationError("Operation cannot have duplicated controls.")

    def validate_parameters(self, operation):
        for parameter in operation.parameters:
            if not isinstance(parameter, int) and not isinstance(parameter, float):
                raise InvalidParameterError(operation.gate, parameter)

    def validate_measurement_operation(self, circuit, operation):
        if len(operation.targets) != 1:
            raise InvalidMeasurementError("Measurement expects exactly one target qubit.")

        if len(operation.controls) != 0:
            raise InvalidMeasurementError("Measurement cannot have controls.")

        if len(operation.parameters) != 1:
            raise InvalidMeasurementError(
                "Measurement expects exactly one classical bit inside parameters."
            )

        qubit_index = operation.targets[0]
        classical_bit_index = operation.parameters[0]

        if not isinstance(qubit_index, int):
            raise InvalidQubitIndexError(qubit_index)

        if qubit_index < 0 or qubit_index >= circuit.qubits:
            raise InvalidQubitIndexError(qubit_index)

        if not isinstance(classical_bit_index, int):
            raise InvalidClassicalBitIndexError(classical_bit_index)

        if classical_bit_index < 0 or classical_bit_index >= circuit.classical_bits:
            raise InvalidClassicalBitIndexError(classical_bit_index)

    def validate_operation_conflicts(self, circuit):
        occupied = {}

        for operation in circuit.get_operations():
            if operation.gate == "MEASURE":
                used_qubits = operation.targets
            else:
                used_qubits = operation.targets + operation.controls

            for qubit_index in used_qubits:
                key = (operation.position, qubit_index)

                if key in occupied:
                    raise OperationConflictError(
                        operation.position,
                        [qubit_index],
                    )

                occupied[key] = operation.id