from fastapi import APIRouter

from composer.circuit.validate_circuit import validate_circuit
from composer.circuit.export_qasm import export_qasm
from composer.circuit.transpile_circuit import transpile_circuit

from schemas.circuit_schema import (
    QasmExportRequestSchema,
    TranspileRequestSchema,
    CircuitValidationRequestSchema,
)
from schemas.simulation_schema import (
    QasmExportResponseSchema,
    TranspileResponseSchema,
    ValidationResponseSchema,
)

from server.api.dependencies import validate_optimization_level
from server.api.presenters.circuit_presenter import schema_to_circuit_model
from server.api.presenters.simulation_presenter import (
    present_qasm_result,
    present_transpile_result,
    present_validation_result,
)

router = APIRouter(prefix="/circuit", tags=["Circuit"])


@router.post("/validate", response_model=ValidationResponseSchema)
def validate(request: CircuitValidationRequestSchema):
    circuit_model = schema_to_circuit_model(request.circuit)

    result = validate_circuit(circuit_model)

    return present_validation_result(result)


@router.post("/qasm", response_model=QasmExportResponseSchema)
def export(request: QasmExportRequestSchema):
    circuit_model = schema_to_circuit_model(request.circuit)

    result = export_qasm(circuit_model)

    return present_qasm_result(result)


@router.post("/transpile", response_model=TranspileResponseSchema)
def transpile(request: TranspileRequestSchema):
    optimization_level = validate_optimization_level(request.optimization_level)
    circuit_model = schema_to_circuit_model(request.circuit)

    result = transpile_circuit(
        circuit_model,
        optimization_level=optimization_level,
    )

    return present_transpile_result(result)
