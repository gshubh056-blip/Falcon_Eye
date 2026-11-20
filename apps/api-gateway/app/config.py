from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

REQUIRED_SETTINGS = (
    "FALCON_ENV",
    "FALCON_NODE_ID",
    "FALCON_SITE_ID",
    "DATABASE_URL",
    "REDIS_URL",
    "MQTT_BROKER",
    "MQTT_PORT",
    "OBJECT_STORE_ENDPOINT",
    "OBJECT_STORE_ACCESS_KEY",
    "OBJECT_STORE_SECRET_KEY",
    "OBJECT_STORE_BUCKET",
    "JWT_SECRET",
    "JWT_ISSUER",
    "JWT_AUDIENCE",
    "LEDGER_SIGNING_KEY_REF",
    "MODEL_DIR",
)


@dataclass(frozen=True)
class Settings:
    falcon_env: str
    falcon_node_id: str
    falcon_site_id: str
    database_url: str
    redis_url: str
    mqtt_broker: str
    mqtt_port: int
    object_store_endpoint: str
    object_store_access_key: str
    object_store_secret_key: str
    object_store_bucket: str
    jwt_secret: str
    jwt_issuer: str
    jwt_audience: str
    ledger_signing_key_ref: str
    rtsp_transport: str
    model_dir: str
    log_level: str


class ConfigurationError(RuntimeError):
    pass


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    values = os.environ if environ is None else environ
    missing = [name for name in REQUIRED_SETTINGS if not values.get(name, "").strip()]
    if missing:
        raise ConfigurationError("Missing required configuration: " + ", ".join(missing))

    try:
        mqtt_port = int(values["MQTT_PORT"])
    except (TypeError, ValueError) as exc:
        raise ConfigurationError("MQTT_PORT must be an integer") from exc

    if not 1 <= mqtt_port <= 65535:
        raise ConfigurationError("MQTT_PORT must be between 1 and 65535")

    jwt_secret = values["JWT_SECRET"].strip()
    object_store_secret = values["OBJECT_STORE_SECRET_KEY"].strip()
    if len(jwt_secret) < 32:
        raise ConfigurationError("JWT_SECRET must contain at least 32 characters")
    if object_store_secret in {"change-me", "local-only-secret"}:
        raise ConfigurationError("OBJECT_STORE_SECRET_KEY must use a local secret")

    return Settings(
        falcon_env=values["FALCON_ENV"].strip(),
        falcon_node_id=values["FALCON_NODE_ID"].strip(),
        falcon_site_id=values["FALCON_SITE_ID"].strip(),
        database_url=values["DATABASE_URL"].strip(),
        redis_url=values["REDIS_URL"].strip(),
        mqtt_broker=values["MQTT_BROKER"].strip(),
        mqtt_port=mqtt_port,
        object_store_endpoint=values["OBJECT_STORE_ENDPOINT"].strip(),
        object_store_access_key=values["OBJECT_STORE_ACCESS_KEY"].strip(),
        object_store_secret_key=object_store_secret,
        object_store_bucket=values["OBJECT_STORE_BUCKET"].strip(),
        jwt_secret=jwt_secret,
        jwt_issuer=values["JWT_ISSUER"].strip(),
        jwt_audience=values["JWT_AUDIENCE"].strip(),
        ledger_signing_key_ref=values["LEDGER_SIGNING_KEY_REF"].strip(),
        rtsp_transport=values.get("RTSP_TRANSPORT", "tcp").strip() or "tcp",
        model_dir=values["MODEL_DIR"].strip(),
        log_level=values.get("LOG_LEVEL", "INFO").strip() or "INFO",
    )
