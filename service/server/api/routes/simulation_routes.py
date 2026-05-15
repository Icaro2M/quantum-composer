from fastapi import APIRouter

from composer.runner.simulate_circuit import simulate_circuit
from composer.runner.get_statevector import get_statevector

from schemas.circuit_schema import (
    SimulationRequestSchema,
    StatevectorRequestSchema,
)
from schemas.simulation_schema import (
    SimulationResponseSchema,
    StatevectorResponseSchema,
)

from server.api.dependencies import validate_shots
from server.api.presenters.circuit_presenter import schema_to_circuit_model
from server.api.presenters.simulation_presenter import (
    present_simulation_result,
    present_statevector_result,
)

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.post("/run", response_model=SimulationResponseSchema)
def run_simulation(request: SimulationRequestSchema):
    shots = validate_shots(request.shots)
    circuit_model = schema_to_circuit_model(request.circuit)

    result = simulate_circuit(
        circuit_model,
        shots=shots,
    )

    return present_simulation_result(result)


@router.post("/statevector", response_model=StatevectorResponseSchema)
def get_circuit_statevector(request: StatevectorRequestSchema):
    circuit_model = schema_to_circuit_model(request.circuit)

    result = get_statevector(circuit_model)

    return present_statevector_result(result)
