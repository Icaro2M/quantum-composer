from qmodel.circuit.gates import (
    GATE_CATALOG,
    get_gate_definition,
    is_supported_gate,
)


def test_single_qubit_gate_h_exists():
    gate = get_gate_definition("H")

    assert gate is not None
    assert gate.name == "H"
    assert gate.target_count == 1
    assert gate.control_count == 0
    assert gate.parameter_count == 0
    assert gate.category == "single_qubit"


def test_multi_qubit_gate_cx_exists():
    gate = get_gate_definition("CX")

    assert gate is not None
    assert gate.name == "CX"
    assert gate.target_count == 1
    assert gate.control_count == 1
    assert gate.parameter_count == 0
    assert gate.category == "multi_qubit"


def test_parametric_gate_rx_exists():
    gate = get_gate_definition("RX")

    assert gate is not None
    assert gate.name == "RX"
    assert gate.target_count == 1
    assert gate.control_count == 0
    assert gate.parameter_count == 1
    assert gate.category == "parametric"


def test_swap_gate_definition():
    gate = get_gate_definition("SWAP")

    assert gate is not None
    assert gate.name == "SWAP"
    assert gate.target_count == 2
    assert gate.control_count == 0
    assert gate.parameter_count == 0
    assert gate.category == "multi_qubit"


def test_u_gate_definition():
    gate = get_gate_definition("U")

    assert gate is not None
    assert gate.name == "U"
    assert gate.target_count == 1
    assert gate.control_count == 0
    assert gate.parameter_count == 3
    assert gate.category == "parametric"


def test_controlled_parametric_gate_definition():
    gate = get_gate_definition("CRX")

    assert gate is not None
    assert gate.name == "CRX"
    assert gate.target_count == 1
    assert gate.control_count == 1
    assert gate.parameter_count == 1
    assert gate.category == "parametric"


def test_unknown_gate_returns_none():
    gate = get_gate_definition("UNKNOWN")

    assert gate is None


def test_is_supported_gate_returns_true_for_existing_gate():
    assert is_supported_gate("H")
    assert is_supported_gate("CX")
    assert is_supported_gate("RX")


def test_is_supported_gate_returns_false_for_unknown_gate():
    assert not is_supported_gate("UNKNOWN")


def test_gate_catalog_contains_expected_gates():
    expected_gates = {
        "I",
        "H",
        "X",
        "Y",
        "Z",
        "S",
        "T",
        "CX",
        "CY",
        "CZ",
        "CH",
        "SWAP",
        "CCX",
        "RX",
        "RY",
        "RZ",
        "P",
        "U",
        "CRX",
        "CRY",
        "CRZ",
    }

    assert expected_gates.issubset(set(GATE_CATALOG.keys()))


def test_gate_definition_helpers():
    cx_gate = get_gate_definition("CX")
    rx_gate = get_gate_definition("RX")
    h_gate = get_gate_definition("H")

    assert cx_gate.is_controlled()
    assert not cx_gate.is_parametric()

    assert not rx_gate.is_controlled()
    assert rx_gate.is_parametric()

    assert not h_gate.is_controlled()
    assert not h_gate.is_parametric()