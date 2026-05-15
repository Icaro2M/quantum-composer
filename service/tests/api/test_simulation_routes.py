import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from schemas.circuit_schema import SimulationRequestSchema, StatevectorRequestSchema
from server.api.routes import simulation_routes


def create_circuit_payload():
    return {
        "qubits": 1,
        "classical_bits": 1,
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
                "gate": "MEASURE",
                "targets": [0],
                "controls": [],
                "parameters": [0],
                "position": 1,
            },
        ],
    }


def test_run_simulation_route_passes_circuit_and_shots(monkeypatch):
    captured = {}

    def fake_simulate_circuit(circuit_model, shots):
        captured["shots"] = shots
        captured["operation_count"] = len(circuit_model.get_operations())
        return {
            "shots": shots,
            "counts": {"0": 5, "1": 3},
        }

    monkeypatch.setattr(
        "server.api.routes.simulation_routes.simulate_circuit",
        fake_simulate_circuit,
    )

    request = SimulationRequestSchema(
        circuit=create_circuit_payload(),
        shots=8,
    )
    result = simulation_routes.run_simulation(request)

    assert result == {
        "shots": 8,
        "counts": {"0": 5, "1": 3},
    }
    assert captured == {
        "shots": 8,
        "operation_count": 2,
    }


def test_run_simulation_route_uses_default_shots(monkeypatch):
    captured = {}

    def fake_simulate_circuit(circuit_model, shots):
        captured["shots"] = shots
        return {
            "shots": shots,
            "counts": {"0": shots},
        }

    monkeypatch.setattr(
        "server.api.routes.simulation_routes.simulate_circuit",
        fake_simulate_circuit,
    )

    request = SimulationRequestSchema(
        circuit=create_circuit_payload(),
    )
    result = simulation_routes.run_simulation(request)

    assert result["shots"] == 1024
    assert captured["shots"] == 1024


def test_run_simulation_route_rejects_invalid_shots():
    request = SimulationRequestSchema(
        circuit=create_circuit_payload(),
        shots=0,
    )

    with pytest.raises(HTTPException) as exc_info:
        simulation_routes.run_simulation(request)

    assert exc_info.value.status_code == 400
    assert "shots must be between 1 and 100000" == exc_info.value.detail


def test_statevector_route_returns_serialized_statevector(monkeypatch):
    def fake_get_statevector(circuit_model):
        return {
            "statevector": [
                {"real": 1.0, "imag": 0.0},
                {"real": 0.0, "imag": 0.0},
            ],
            "probabilities": {"0": 1.0, "1": 0.0},
        }

    monkeypatch.setattr(
        "server.api.routes.simulation_routes.get_statevector",
        fake_get_statevector,
    )

    request = StatevectorRequestSchema(
        circuit=create_circuit_payload(),
    )
    result = simulation_routes.get_circuit_statevector(request)

    assert result == {
        "statevector": [
            {"real": 1.0, "imag": 0.0},
            {"real": 0.0, "imag": 0.0},
        ],
        "probabilities": {"0": 1.0, "1": 0.0},
    }


def test_statevector_route_rejects_invalid_request_body():
    with pytest.raises(ValidationError):
        StatevectorRequestSchema(circuit={"qubits": 1})
