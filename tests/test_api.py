import sys
from pathlib import Path

import pytest

API_GATEWAY_APP = Path(__file__).resolve().parents[1] / "apps" / "api-gateway"
sys.path.insert(0, str(API_GATEWAY_APP))

from app.main import (  # noqa: E402
    alert_actions_store,
    alerts_store,
    app,
    completed_mutations,
)
from fastapi.testclient import TestClient  # noqa: E402


def demo_environment(monkeypatch) -> None:
    values = {
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
        "MODEL_DIR": "./models/registry",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)


def reset_alert_store() -> None:
    alerts_store.clear()
    alerts_store["synthetic-intrusion-001"] = {
        "id": "synthetic-intrusion-001",
        "severity": "high",
        "status": "new",
        "title": "Synthetic perimeter intrusion",
        "description": "Deterministic test event; no real camera or person.",
        "created_at": "2026-11-19T08:42:09+05:30",
        "camera_id": "synthetic-camera-001",
        "event_id": "synthetic-event-001",
        "escalation_level": 0,
        "false_positive": False,
        "false_positive_reason": None,
    }
    alert_actions_store.clear()
    alert_actions_store["synthetic-intrusion-001"] = []
    completed_mutations.clear()


def test_health_is_synthetic(monkeypatch):
    demo_environment(monkeypatch)
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "synthetic"}


def test_preview_origin_can_call_api(monkeypatch):
    demo_environment(monkeypatch)
    origin = "http://127.0.0.1:4173"
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/alerts",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


def test_camera_frame_person_analysis_persists(monkeypatch, tmp_path):
    demo_environment(monkeypatch)
    monkeypatch.setenv("FALCON_DETECTION_DB_PATH", str(tmp_path / "detections.sqlite3"))
    import base64

    import cv2
    import numpy as np

    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    _, encoded = cv2.imencode(".jpg", frame)
    body = {
        "camera_id": "browser-camera-001",
        "captured_at": "2026-11-20T10:15:00+05:30",
        "image_jpeg_base64": base64.b64encode(encoded.tobytes()).decode("ascii"),
        "idempotency_key": "camera-frame-test-1",
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/camera-frame", json=body)
        records = client.get("/api/v1/detections")

    assert response.status_code == 200
    assert response.json()["item"]["model_id"] == "opencv-hog-person"
    assert isinstance(response.json()["item"]["person_count"], int)
    assert len(records.json()["items"]) >= 1


def test_detection_records_are_persisted_and_deduplicated(monkeypatch, tmp_path):
    demo_environment(monkeypatch)
    monkeypatch.setenv("FALCON_DETECTION_DB_PATH", str(tmp_path / "detections.sqlite3"))
    body = {
        "camera_id": "browser-camera-001",
        "detected_at": "2026-11-20T10:15:00+05:30",
        "model_id": "approved-test-model",
        "model_version": "1.0.0",
        "detections": [
            {
                "label": "person",
                "confidence": 0.91,
                "x": 0.1,
                "y": 0.2,
                "width": 0.3,
                "height": 0.6,
            },
            {
                "label": "vehicle",
                "confidence": 0.88,
                "x": 0.5,
                "y": 0.4,
                "width": 0.2,
                "height": 0.25,
            },
        ],
        "idempotency_key": "detection-test-1",
    }
    with TestClient(app) as client:
        first = client.post("/api/v1/detections", json=body)
        repeated = client.post("/api/v1/detections", json=body)
        records = client.get("/api/v1/detections")
        events_response = client.get("/api/v1/events")

    assert first.status_code == 200
    assert repeated.status_code == 200
    assert repeated.json()["deduplicated"] is True
    assert first.json()["item"]["person_count"] == 1
    assert first.json()["item"]["vehicle_count"] == 1
    assert len(records.json()["items"]) == 1
    assert any(
        event["event_type"] == "camera_detection"
        for event in events_response.json()["items"]
    )


def test_alert_contract_returns_labeled_test_alert(monkeypatch):
    demo_environment(monkeypatch)
    with TestClient(app) as client:
        response = client.get("/api/v1/alerts")

    assert response.status_code == 200
    alert = response.json()["items"][0]
    assert alert["id"] == "synthetic-intrusion-001"
    assert alert["status"] == "new"
    assert "Synthetic" in alert["title"]


@pytest.mark.parametrize(
    ("path", "item_field"),
    [
        ("/api/v1/cameras", "camera_type"),
        ("/api/v1/events", "event_type"),
        ("/api/v1/devices", "hostname"),
    ],
)
def test_synthetic_resource_contracts(monkeypatch, path: str, item_field: str):
    demo_environment(monkeypatch)
    with TestClient(app) as client:
        response = client.get(path)

    assert response.status_code == 200
    assert item_field in response.json()["items"][0]


def test_alert_detail_and_action_history(monkeypatch):
    demo_environment(monkeypatch)
    reset_alert_store()
    with TestClient(app) as client:
        response = client.get("/api/v1/alerts/synthetic-intrusion-001")

    assert response.status_code == 200
    assert response.json()["item"]["status"] == "new"
    assert response.json()["actions"] == []


def test_alert_acknowledge_is_idempotent(monkeypatch):
    demo_environment(monkeypatch)
    reset_alert_store()
    body = {
        "actor": "demo-operator",
        "purpose": "Operator alert review",
        "idempotency_key": "ack-test-1",
    }
    with TestClient(app) as client:
        first = client.post(
            "/api/v1/alerts/synthetic-intrusion-001/acknowledge",
            json=body,
        )
        repeated = client.post(
            "/api/v1/alerts/synthetic-intrusion-001/acknowledge",
            json=body,
        )

    assert first.status_code == 200
    assert repeated.status_code == 200
    assert first.json()["item"]["status"] == "acknowledged"
    assert repeated.json() == first.json()


def test_false_positive_requires_reason(monkeypatch):
    demo_environment(monkeypatch)
    reset_alert_store()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/alerts/synthetic-intrusion-001/false-positive",
            json={
                "actor": "demo-operator",
                "purpose": "Operator alert review",
                "reason": "   ",
                "idempotency_key": "false-positive-test-1",
            },
        )

    assert response.status_code == 422
    assert response.json()["code"] == "reason_required"


def test_alert_transition_conflict(monkeypatch):
    demo_environment(monkeypatch)
    reset_alert_store()
    with TestClient(app) as client:
        first = client.post(
            "/api/v1/alerts/synthetic-intrusion-001/resolve",
            json={
                "actor": "demo-operator",
                "purpose": "Operator alert review",
                "idempotency_key": "resolve-test-1",
            },
        )
        conflict = client.post(
            "/api/v1/alerts/synthetic-intrusion-001/acknowledge",
            json={
                "actor": "demo-operator",
                "purpose": "Operator alert review",
                "idempotency_key": "ack-test-2",
            },
        )

    assert first.status_code == 200
    assert conflict.status_code == 409
    assert conflict.json()["code"] == "invalid_transition"


def test_missing_secret_prevents_startup(monkeypatch):
    demo_environment(monkeypatch)
    monkeypatch.delenv("JWT_SECRET")

    try:
        with TestClient(app):
            pass
    except RuntimeError as exc:
        assert "JWT_SECRET" in str(exc)
    else:
        raise AssertionError("startup should fail without the required JWT secret")
