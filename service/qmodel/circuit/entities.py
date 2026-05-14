from qmodel.circuit.exceptions import (
    DuplicateOperationIdError,
    OperationNotFoundError,
)


class QuantumCircuitModel:

    def __init__(self, qubits, classical_bits):
        self.qubits = qubits
        self.classical_bits = classical_bits
        self.operations = []

    def get_qubit_count(self):
        return self.qubits

    def get_classical_bit_count(self):
        return self.classical_bits
    
    def get_operations(self):
        return list(self.operations)
    
    def get_operations_ordered(self):
        return sorted(self.operations, key=lambda op: op.position)

    def add_operation(self, operation):
        if self.has_operation(operation.id):
            raise DuplicateOperationIdError(operation.id)

        self.operations.append(operation)

    def remove_operation(self, operation_id):
        for i in range(len(self.operations)):
            if self.operations[i].id == operation_id:
                self.operations.pop(i)
                return

        raise OperationNotFoundError(operation_id)
    
    def get_operation(self, operation_id):
        for operation in self.operations:
            if operation.id == operation_id:
                return operation

        return None
    
    def clear_operations(self):
        self.operations = []
    
    def has_operation(self, operation_id):
        return self.get_operation(operation_id) is not None


class QuantumOperation:

    def __init__(self, id, gate, targets, controls, parameters, position):
        self.id = id
        self.gate = gate
        self.targets = targets
        self.controls = controls
        self.parameters = parameters
        self.position = position
    
