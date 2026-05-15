import pytest
from fastapi import HTTPException

from server.api.dependencies import validate_optimization_level, validate_shots


def test_validate_shots_returns_value_inside_configured_range():
    assert validate_shots(1) == 1
    assert validate_shots(1024) == 1024
    assert validate_shots(100000) == 100000


@pytest.mark.parametrize("shots", [0, 100001])
def test_validate_shots_raises_for_value_outside_configured_range(shots):
    with pytest.raises(HTTPException) as exc_info:
        validate_shots(shots)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "shots must be between 1 and 100000"


def test_validate_optimization_level_returns_value_inside_configured_range():
    assert validate_optimization_level(0) == 0
    assert validate_optimization_level(1) == 1
    assert validate_optimization_level(3) == 3


@pytest.mark.parametrize("optimization_level", [-1, 4])
def test_validate_optimization_level_raises_for_value_outside_configured_range(
    optimization_level,
):
    with pytest.raises(HTTPException) as exc_info:
        validate_optimization_level(optimization_level)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "optimization_level must be between 0 and 3"
