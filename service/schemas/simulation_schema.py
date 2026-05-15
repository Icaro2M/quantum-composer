from pydantic import BaseModel


class ComplexAmplitudeSchema(BaseModel):
    real: float
    imag: float


class SimulationResponseSchema(BaseModel):
    shots: int
    counts: dict[str, int]


class StatevectorResponseSchema(BaseModel):
    statevector: list[ComplexAmplitudeSchema]
    probabilities: dict[str, float]


class QasmExportResponseSchema(BaseModel):
    format: str
    qasm: str


class TranspileResponseSchema(BaseModel):
    optimization_level: int
    depth: int
    width: int
    size: int
    operations: dict[str, int]
    qasm: str


class ValidationResponseSchema(BaseModel):
    valid: bool
    errors: list[str]