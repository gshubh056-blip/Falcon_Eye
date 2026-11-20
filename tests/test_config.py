import sys
from pathlib import Path

import pytest

API_GATEWAY_APP = Path(__file__).resolve().parents[1] / "apps" / "api-gateway"
sys.path.insert(0, str(API_GATEWAY_APP))

from app.config import ConfigurationError, load_settings  # noqa: E402


def valid_environment() -> dict[str, str]:
    return {
        "FALCON_ENV": "demo",
        "FALCON_NODE_ID": "edge-node-01",
        "FALCON_SITE_ID": "demo-bop",
        "DATABASE_URL": "postgresql+psycopg://falcon:falcon@localhost:5432/falcon",
        "REDIS_URL": "redis://localhost:6379/0",
        "MQTT_BROKER": "localhost",
        "MQTT_PORT": "1883",
        "OBJECT_STORE_ENDPOINT": "http://localhost:9000",
        "OBJECT_STORE_ACCESS_KEY": "falconadmin",
        "OBJECT_STORE_SECRET_KEY": "local-test-object-store-secret",
        "OBJECT_STORE_BUCKET": "falcon-evidence",
        "JWT_SECRET": "local-test-jwt-secret-at-least-32-chars",
        "JWT_ISSUER": "http://localhost:8000",
        "JWT_AUDIENCE": "falcon-dashboard",
        "LEDGER_SIGNING_KEY_REF": "./keys/edge-private.pem",
        "RTSP_TRANSPORT": "tcp",
        "MODEL_DIR": "./models/registry",
        "LOG_LEVEL": "INFO",
    }


def test_load_settings_accepts_complete_local_environment():
    settings = load_settings(valid_environment())

    assert settings.falcon_env == "demo"
    assert settings.mqtt_port == 1883


@pytest.mark.parametrize("name", ["FALCON_ENV", "JWT_SECRET", "DATABASE_URL"])
def test_missing_required_setting_fails_startup(name: str):
    environment = valid_environment()
    environment.pop(name)

    with pytest.raises(ConfigurationError, match="Missing required configuration"):
        load_settings(environment)


def test_short_jwt_secret_fails_startup():
    environment = valid_environment()
    environment["JWT_SECRET"] = "too-short"

    with pytest.raises(ConfigurationError, match="at least 32 characters"):
        load_settings(environment)


def test_invalid_mqtt_port_fails_startup():
    environment = valid_environment()
    environment["MQTT_PORT"] = "not-a-port"

    with pytest.raises(ConfigurationError, match="must be an integer"):
        load_settings(environment)
