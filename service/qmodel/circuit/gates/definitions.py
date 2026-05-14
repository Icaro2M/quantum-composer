from dataclasses import dataclass


@dataclass(frozen=True)
class GateDefinition:
    name: str
    target_count: int
    control_count: int
    parameter_count: int
    category: str

    def is_controlled(self):
        return self.control_count > 0

    def is_parametric(self):
        return self.parameter_count > 0