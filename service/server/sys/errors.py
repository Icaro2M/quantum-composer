from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from qmodel.circuit.exceptions import CircuitError


async def circuit_error_handler(
    request: Request,
    exc: CircuitError,
):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "details": [],
        },
    )


async def value_error_handler(
    request: Request,
    exc: ValueError,
):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "details": [],
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        CircuitError,
        circuit_error_handler,
    )

    app.add_exception_handler(
        ValueError,
        value_error_handler,
    )