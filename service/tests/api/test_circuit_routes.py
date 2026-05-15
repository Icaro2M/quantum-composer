import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from schemas.circuit_schema import (
    CircuitValidationRequestSchema,
    QasmExportRequestSchema,
    TranspileRequestSchema,
)
from server.api.routes import circuit_routes


def create_circuit_payload():
    return {
        "qubits": 2,
        "classical_bits": 2,
        "operations": [
            {
                "id": "op-1",
                "gate": "H",
                "targets": [0],
                "controls": [],
                "parameters": [],
                "position": 0,
            },
            {
                "id": "op-2",
                "gate": "CX",
                "targets": [1],
                "controls": [0],
                "parameters": [],
                "position": 1,
            },
        ],
    }


def test_validate_route_converts_schema_and_returns_validation_result(monkeypatch):
    captured = {}

    def fake_validate_circuit(circuit_model):
        captured["qubits"] = circuit_model.get_qubit_count()
        captured["classical_bits"] = circuit_model.get_classical_bit_count()
        captured["operations"] = circuit_model.get_operations_ordered()
        return {
            "valid": True,
            "errors": [],
        }

    monkeypatch.setattr(
        "server.api.routes.circuit_routes.validate_circuit",
        fake_validate_circuit,
    )

    request = CircuitValidationRequestSchema(
        circuit=create_circuit_payload(),
    )
    result = circuit_routes.validate(request)

    assert result == {
        "valid": True,
        "errors": [],
    }
    assert captured["qubits"] == 2
    assert captured["classical_bits"] == 2
    assert [operation.gate for operation in captured["operations"]] == ["H", "CX"]


def test_qasm_route_returns_exported_qasm(monkeypatch):
    def fake_export_qasm(circuit_model):
        return {
            "format": "OPENQASM 3.0",
            "qasm": "OPENQASM 3.0;",
        }

    monkeypatch.setattr(
        "server.api.routes.circuit_routes.export_qasm",
        fake_export_qasm,
    )

    request = QasmExportRequestSchema(
        circuit=create_circuit_payload(),
    )
    result = circuit_routes.export(request)

    assert result == {
        "format": "OPENQASM 3.0",
        "qasm": "OPENQASM 3.0;",
    }


def test_transpile_route_passes_optimization_level(monkeypatch):
    captured = {}

    def fake_transpile_circuit(circuit_model, optimization_level):
        captured["optimization_level"] = optimization_level
        return {
            "optimization_level": optimization_level,
            "depth": 2,
            "width": 4,
            "size": 4,
            "operations": {"h": 1, "cx": 1},
            "qasm": "OPENQASM 3.0;",
        }

    monkeypatch.setattr(
        "server.api.routes.circuit_routes.transpile_circuit",
        fake_transpile_circuit,
    )

    request = TranspileRequestSchema(
        circuit=create_circuit_payload(),
        optimization_level=3,
    )
    result = circuit_routes.transpile(request)

    assert result["optimization_level"] == 3
    assert result["operations"] == {"h": 1, "cx": 1}
    assert captured["optimization_level"] == 3


def test_transpile_route_rejects_invalid_optimization_level():
    request = TranspileRequestSchema(
        circuit=create_circuit_payload(),
        optimization_level=4,
    )

    with pytest.raises(HTTPException) as exc_info:
        circuit_routes.transpile(request)

    assert exc_info.value.status_code == 400
    assert "optimization_level must be between 0 and 3" == exc_info.value.detail


def test_validate_route_rejects_invalid_request_body():
    with pytest.raises(ValidationError):
        CircuitValidationRequestSchema(circuit={"qubits": 1})
