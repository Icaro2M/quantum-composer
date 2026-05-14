from qmodel.circuit.gates.definitions import GateDefinition


RX_GATE = GateDefinition(
    name="RX",
    target_count=1,
    control_count=0,
    parameter_count=1,
    category="parametric",
)

RY_GATE = GateDefinition(
    name="RY",
    target_count=1,
    control_count=0,
    parameter_count=1,
    category="parametric",
)

RZ_GATE = GateDefinition(
    name="RZ",
    target_count=1,
    control_count=0,
    parameter_count=1,
    category="parametric",
)

P_GATE = GateDefinition(
    name="P",
    target_count=1,
    control_count=0,
    parameter_count=1,
    category="parametric",
)

U_GATE = GateDefinition(
    name="U",
    target_count=1,
    control_count=0,
    parameter_count=3,
    category="parametric",
)

CRX_GATE = GateDefinition(
    name="CRX",
    target_count=1,
    control_count=1,
    parameter_count=1,
    category="parametric",
)

CRY_GATE = GateDefinition(
    name="CRY",
    target_count=1,
    control_count=1,
    parameter_count=1,
    category="parametric",
)

CRZ_GATE = GateDefinition(
    name="CRZ",
    target_count=1,
    control_count=1,
    parameter_count=1,
    category="parametric",
)


PARAMETRIC_GATES = {
    gate.name: gate
    for gate in [
        RX_GATE,
        RY_GATE,
        RZ_GATE,
        P_GATE,
        U_GATE,
        CRX_GATE,
        CRY_GATE,
        CRZ_GATE,
    ]
}