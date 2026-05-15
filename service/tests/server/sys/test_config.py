from server.sys.config import AppConfig, config


def test_default_config_values():
    assert config == AppConfig()
    assert config.app_name == "Quantum Composer API"
    assert config.app_version == "0.1.0"
    assert config.default_shots == 1024
    assert config.min_shots == 1
    assert config.max_shots == 100000
    assert config.default_optimization_level == 1
    assert config.min_optimization_level == 0
    assert config.max_optimization_level == 3
