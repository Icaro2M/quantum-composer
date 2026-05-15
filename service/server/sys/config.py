from pydantic import BaseModel


class AppConfig(BaseModel):
    app_name: str = "Quantum Composer API"
    app_version: str = "0.1.0"
    default_shots: int = 1024
    min_shots: int = 1
    max_shots: int = 100000
    default_optimization_level: int = 1
    min_optimization_level: int = 0
    max_optimization_level: int = 3


config = AppConfig()