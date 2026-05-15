import asyncio

from fastapi import FastAPI

from qmodel.circuit.exceptions import InvalidGateError
from server.sys.errors import (
    circuit_error_handler,
    register_exception_handlers,
    value_error_handler,
)


def test_circuit_error_handler_returns_standard_error_payload():
    response = asyncio.run(
        circuit_error_handler(
            request=None,
            exc=InvalidGateError("UNKNOWN"),
        )
    )

    assert response.status_code == 400
    assert response.body == (
        b'{"error":"InvalidGateError",'
        b'"message":"Invalid or unsupported gate: UNKNOWN",'
        b'"details":[]}'
    )


def test_value_error_handler_returns_standard_error_payload():
    response = asyncio.run(
        value_error_handler(
            request=None,
            exc=ValueError("bad value"),
        )
    )

    assert response.status_code == 400
    assert response.body == (
        b'{"error":"ValueError","message":"bad value","details":[]}'
    )


def test_register_exception_handlers_adds_domain_and_value_error_handlers():
    app = FastAPI()

    register_exception_handlers(app)

    assert app.exception_handlers[ValueError] is value_error_handler
    assert app.exception_handlers[InvalidGateError.__mro__[1]] is circuit_error_handler
