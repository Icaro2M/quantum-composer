from server.main import app, root
from server.sys.config import config


def test_app_uses_configured_metadata():
    assert app.title == config.app_name
    assert app.version == config.app_version


def test_root_returns_api_status_and_version():
    assert root() == {
        "name": config.app_name,
        "version": config.app_version,
        "status": "running",
    }
