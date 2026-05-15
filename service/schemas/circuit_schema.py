from pydantic import BaseModel, Field


class OperationSchema(BaseModel):
    id: str
    gate: str
    targets: list[int] = Field(default_factory=list)
    controls: list[int] = Field(default_factory=list)
    parameters: list[int | float] = Field(default_factory=list)
    position: int


class CircuitSchema(BaseModel):
    qubits: int
    classical_bits: int
    operations: list[OperationSchema] = Field(default_factory=list)


class SimulationRequestSchema(BaseModel):
    circuit: CircuitSchema
    shots: int = 1024


class StatevectorRequestSchema(BaseModel):
    circuit: CircuitSchema


class CircuitValidationRequestSchema(BaseModel):
    circuit: CircuitSchema


class QasmExportRequestSchema(BaseModel):
    circuit: CircuitSchema


class TranspileRequestSchema(BaseModel):
    circuit: CircuitSchema
    optimization_level: int = 1