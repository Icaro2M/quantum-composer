from qmodel.circuit.gates.definitions import GateDefinition


H_GATE = GateDefinition(
    name="H",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)

X_GATE = GateDefinition(
    name="X",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)

Y_GATE = GateDefinition(
    name="Y",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)

Z_GATE = GateDefinition(
    name="Z",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)

S_GATE = GateDefinition(
    name="S",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)

T_GATE = GateDefinition(
    name="T",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)

I_GATE = GateDefinition(
    name="I",
    target_count=1,
    control_count=0,
    parameter_count=0,
    category="single_qubit",
)


SINGLE_QUBIT_GATES = {
    gate.name: gate
    for gate in [
        H_GATE,
        X_GATE,
        Y_GATE,
        Z_GATE,
        S_GATE,
        T_GATE,
        I_GATE,
    ]
}