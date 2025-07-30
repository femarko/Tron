from src.bootstrap.config import Config, settings


def test_config_creation():
    config = Config()
    assert config.db_url
    assert config.mode
    assert config.mode in {"dev", "test"}


def test_config_values():
    assert settings.db_url