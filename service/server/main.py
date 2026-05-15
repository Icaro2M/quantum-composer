from fastapi import FastAPI

from server.api.routes.circuit_routes import router as circuit_router
from server.api.routes.simulation_routes import router as simulation_router
from server.sys.config import config
from server.sys.errors import register_exception_handlers

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
)

register_exception_handlers(app)

app.include_router(circuit_router)
app.include_router(simulation_router)


@app.get("/")
def root():
    return {
        "name": config.app_name,
        "version": config.app_version,
        "status": "running",
    }