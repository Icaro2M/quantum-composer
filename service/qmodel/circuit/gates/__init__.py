from qmodel.circuit.gates.single_qubit import SINGLE_QUBIT_GATES
from qmodel.circuit.gates.multi_qubit import MULTI_QUBIT_GATES
from qmodel.circuit.gates.parametric import PARAMETRIC_GATES


GATE_CATALOG = {
    **SINGLE_QUBIT_GATES,
    **MULTI_QUBIT_GATES,
    **PARAMETRIC_GATES,
}


def get_gate_definition(gate_name):
    return GATE_CATALOG.get(gate_name)


def is_supported_gate(gate_name):
    return gate_name in GATE_CATALOG