from qmodel.circuit.gates.definitions import GateDefinition


CX_GATE = GateDefinition(
    name="CX",
    target_count=1,
    control_count=1,
    parameter_count=0,
    category="multi_qubit",
)

CZ_GATE = GateDefinition(
    name="CZ",
    target_count=1,
    control_count=1,
    parameter_count=0,
    category="multi_qubit",
)

CY_GATE = GateDefinition(
    name="CY",
    target_count=1,
    control_count=1,
    parameter_count=0,
    category="multi_qubit",
)

CH_GATE = GateDefinition(
    name="CH",
    target_count=1,
    control_count=1,
    parameter_count=0,
    category="multi_qubit",
)

SWAP_GATE = GateDefinition(
    name="SWAP",
    target_count=2,
    control_count=0,
    parameter_count=0,
    category="multi_qubit",
)

CCX_GATE = GateDefinition(
    name="CCX",
    target_count=1,
    control_count=2,
    parameter_count=0,
    category="multi_qubit",
)


MULTI_QUBIT_GATES = {
    gate.name: gate
    for gate in [
        CX_GATE,
        CZ_GATE,
        CY_GATE,
        CH_GATE,
        SWAP_GATE,
        CCX_GATE,
    ]
}