from fastapi import HTTPException

from server.sys.config import config


def validate_shots(shots: int):
    if shots < config.min_shots or shots > config.max_shots:
        raise HTTPException(
            status_code=400,
            detail=f"shots must be between {config.min_shots} and {config.max_shots}",
        )

    return shots


def validate_optimization_level(optimization_level: int):
    if (
        optimization_level < config.min_optimization_level
        or optimization_level > config.max_optimization_level
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "optimization_level must be between "
                f"{config.min_optimization_level} and "
                f"{config.max_optimization_level}"
            ),
        )

    return optimization_level