from __future__ import annotations

import asyncio
import sqlite3
import time
from base64 import b64decode
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .config import ConfigurationError, load_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        load_settings()
    except ConfigurationError as exc:
        raise RuntimeError(str(exc)) from exc
    init_detection_database()
    yield


app = FastAPI(title="FALCON API Gateway", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:4173",
        "http://localhost:4173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


class AlertConnectionManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    async def broadcast(self, message: dict[str, object]) -> None:
        stale: list[WebSocket] = []
        for connection in tuple(self._connections):
            with suppress(Exception):
                await connection.send_json(message)
            if connection not in self._connections:
                stale.append(connection)
        for connection in stale:
            self.disconnect(connection)


manager = AlertConnectionManager()


class AlertMutation(BaseModel):
    actor: str = Field(min_length=1, max_length=128)
    purpose: str = Field(min_length=1, max_length=256)
    reason: str | None = Field(default=None, max_length=1000)
    idempotency_key: str = Field(min_length=1, max_length=128)


class DetectionBox(BaseModel):
    label: str = Field(min_length=1, max_length=64)
    confidence: float = Field(ge=0.0, le=1.0)
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)
    width: float = Field(gt=0.0, le=1.0)
    height: float = Field(gt=0.0, le=1.0)


class DetectionSubmission(BaseModel):
    camera_id: str = Field(min_length=1, max_length=128)
    detected_at: str = Field(min_length=1, max_length=64)
    model_id: str = Field(min_length=1, max_length=128)
    model_version: str = Field(min_length=1, max_length=128)
    detections: list[DetectionBox] = Field(max_length=500)
    idempotency_key: str = Field(min_length=1, max_length=128)


class CameraFrameSubmission(BaseModel):
    camera_id: str = Field(min_length=1, max_length=128)
    captured_at: str = Field(min_length=1, max_length=64)
    image_jpeg_base64: str = Field(min_length=1, max_length=3_000_000)
    idempotency_key: str = Field(min_length=1, max_length=128)


class CameraConfigSubmission(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    source_type: str = Field(pattern=r"^(browser|usb|phone|video|rtsp|onvif)$")
    source_url: str = Field(max_length=2048)


def detection_database_path() -> Path:
    import os

    configured = os.getenv("FALCON_DETECTION_DB_PATH")
    if configured:
        return Path(configured)
    return Path(__file__).resolve().parents[3] / "data" / "falcon-detections.sqlite3"


def init_detection_database() -> None:
    database_path = detection_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS camera_configs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_url TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS detections (
                id TEXT PRIMARY KEY,
                camera_id TEXT NOT NULL,
                detected_at TEXT NOT NULL,
                model_id TEXT NOT NULL,
                model_version TEXT NOT NULL,
                detections_json TEXT NOT NULL,
                person_count INTEGER NOT NULL,
                vehicle_count INTEGER NOT NULL,
                idempotency_key TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_detections_detected_at "
            "ON detections(detected_at)"
        )


def detection_rows(limit: int = 100) -> list[dict[str, object]]:
    import json

    init_detection_database()
    with sqlite3.connect(detection_database_path()) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, camera_id, detected_at, model_id, model_version,
                   detections_json, person_count, vehicle_count,
                   idempotency_key, created_at
            FROM detections
            ORDER BY detected_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [
        {
            **dict(row),
            "detections": json.loads(str(row["detections_json"])),
        }
        for row in rows
    ]


def detect_people(frame: np.ndarray) -> list[DetectionBox]:
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    height, width = frame.shape[:2]
    if width > 640:
        scale = 640 / width
        frame = cv2.resize(frame, (640, max(1, round(height * scale))))
    boxes, weights = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05,
    )

    detections: list[DetectionBox] = []
    frame_height, frame_width = frame.shape[:2]
    for (x, y, box_width, box_height), weight in zip(boxes, weights, strict=False):
        confidence = min(1.0, max(0.0, float(weight)))
        if confidence < 0.5:
            continue
        detections.append(
            DetectionBox(
                label="person",
                confidence=confidence,
                x=max(0.0, min(1.0, float(x) / frame_width)),
                y=max(0.0, min(1.0, float(y) / frame_height)),
                width=max(0.0, min(1.0, float(box_width) / frame_width)),
                height=max(0.0, min(1.0, float(box_height) / frame_height)),
            )
        )
    return detections


alerts_store: dict[str, dict[str, object]] = {
    "synthetic-intrusion-001": {
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
}
alert_actions_store: dict[str, list[dict[str, object]]] = {"synthetic-intrusion-001": []}
completed_mutations: dict[str, dict[str, object]] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "mode": "synthetic"}


@app.get("/api/v1/alerts")
async def alerts() -> dict[str, list[dict[str, object]]]:
    return {"items": [deepcopy(item) for item in alerts_store.values()]}


@app.get("/api/v1/alerts/{alert_id}", response_model=None)
async def alert_detail(alert_id: str) -> dict[str, object] | JSONResponse:
    alert = alerts_store.get(alert_id)
    if alert is None:
        return JSONResponse(
            status_code=404,
            content={"detail": "Alert not found", "code": "alert_not_found"},
        )
    return {
        "item": deepcopy(alert),
        "actions": deepcopy(alert_actions_store.get(alert_id, [])),
    }


def mutate_alert(
    alert_id: str,
    action: str,
    mutation: AlertMutation,
) -> dict[str, object] | JSONResponse:
    alert = alerts_store.get(alert_id)
    if alert is None:
        return JSONResponse(
            status_code=404,
            content={"detail": "Alert not found", "code": "alert_not_found"},
        )

    previous = completed_mutations.get(mutation.idempotency_key)
    if previous is not None:
        return deepcopy(previous)

    previous_status = str(alert["status"])
    if action == "acknowledge":
        if previous_status != "new":
            return JSONResponse(
                status_code=409,
                content={
                    "detail": "Only new alerts can be acknowledged",
                    "code": "invalid_transition",
                },
            )
        alert["status"] = "acknowledged"
    elif action == "escalate":
        if previous_status not in {"new", "acknowledged"}:
            return JSONResponse(
                status_code=409,
                content={
                    "detail": "Resolved alerts cannot be escalated",
                    "code": "invalid_transition",
                },
            )
        alert["status"] = "escalated"
        escalation_level = alert["escalation_level"]
        if not isinstance(escalation_level, int):
            raise RuntimeError("Alert escalation level must be an integer")
        alert["escalation_level"] = escalation_level + 1
    elif action == "resolve":
        if previous_status not in {"new", "acknowledged", "escalated"}:
            return JSONResponse(
                status_code=409,
                content={"detail": "This alert is already closed", "code": "invalid_transition"},
            )
        alert["status"] = "resolved"
    elif action == "false_positive":
        if not mutation.reason or not mutation.reason.strip():
            return JSONResponse(
                status_code=422,
                content={
                    "detail": "A false-positive reason is required",
                    "code": "reason_required",
                },
            )
        if previous_status in {"resolved", "closed"}:
            return JSONResponse(
                status_code=409,
                content={
                    "detail": "Resolved alerts cannot be marked false positive",
                    "code": "invalid_transition",
                },
            )
        alert["status"] = "false_positive"
        alert["false_positive"] = True
        alert["false_positive_reason"] = mutation.reason.strip()

    action_record = {
        "alert_id": alert_id,
        "actor": mutation.actor,
        "purpose": mutation.purpose,
        "action": action,
        "reason": mutation.reason,
        "previous_status": previous_status,
        "new_status": alert["status"],
        "acted_at": "2026-11-19T08:42:09+05:30",
    }
    alert_actions_store.setdefault(alert_id, []).append(action_record)
    result: dict[str, object] = {"item": deepcopy(alert), "action": deepcopy(action_record)}
    completed_mutations[mutation.idempotency_key] = result
    return result


@app.post("/api/v1/alerts/{alert_id}/acknowledge", response_model=None)
async def acknowledge_alert(
    alert_id: str, mutation: AlertMutation
) -> dict[str, object] | JSONResponse:
    return mutate_alert(alert_id, "acknowledge", mutation)


@app.post("/api/v1/alerts/{alert_id}/escalate", response_model=None)
async def escalate_alert(
    alert_id: str, mutation: AlertMutation
) -> dict[str, object] | JSONResponse:
    return mutate_alert(alert_id, "escalate", mutation)


@app.post("/api/v1/alerts/{alert_id}/resolve", response_model=None)
async def resolve_alert(alert_id: str, mutation: AlertMutation) -> dict[str, object] | JSONResponse:
    return mutate_alert(alert_id, "resolve", mutation)


@app.post("/api/v1/alerts/{alert_id}/false-positive", response_model=None)
async def false_positive_alert(
    alert_id: str, mutation: AlertMutation
) -> dict[str, object] | JSONResponse:
    return mutate_alert(alert_id, "false_positive", mutation)


@app.get("/api/v1/cameras")
async def cameras() -> dict[str, list[dict[str, object]]]:
    return {
        "items": [
            {
                "id": "synthetic-camera-001",
                "name": "North Perimeter Test Camera",
                "status": "local_preview",
                "protocol": "file",
                "camera_type": "visible",
                "label": "TEST DATA",
            }
        ]
    }


@app.get("/api/v1/detections")
async def detections() -> dict[str, list[dict[str, object]]]:
    return {"items": detection_rows()}


@app.get("/api/v1/camera-configs")
async def camera_configs() -> dict[str, list[dict[str, object]]]:
    init_detection_database()
    with sqlite3.connect(detection_database_path()) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, name, source_type, source_url, status, created_at, updated_at
            FROM camera_configs
            ORDER BY created_at DESC
            """
        ).fetchall()
    return {"items": [dict(row) for row in rows]}


@app.post("/api/v1/camera-configs", response_model=None)
async def add_camera_config(
    submission: CameraConfigSubmission,
) -> dict[str, object] | JSONResponse:
    source_type = submission.source_type
    source_url = submission.source_url.strip()
    if source_type in {"rtsp", "onvif"}:
        return JSONResponse(
            status_code=501,
            content={
                "detail": f"{source_type.upper()} capture requires a tested edge adapter.",
                "code": "source_not_implemented",
            },
        )
    if source_type == "phone" and not source_url:
        return JSONResponse(
            status_code=422,
            content={"detail": "Phone stream URL is required", "code": "source_url_required"},
        )
    camera_id = str(uuid4())
    now = datetime.now(UTC).isoformat()
    init_detection_database()
    with sqlite3.connect(detection_database_path()) as connection:
        connection.execute(
            """
            INSERT INTO camera_configs
                (id, name, source_type, source_url, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                camera_id,
                submission.name,
                source_type,
                source_url,
                "configured",
                now,
                now,
            ),
        )
    return {
        "item": {
            "id": camera_id,
            "name": submission.name,
            "source_type": source_type,
            "source_url": source_url,
            "status": "configured",
            "created_at": now,
            "updated_at": now,
        }
    }


@app.delete("/api/v1/camera-configs/{camera_id}", response_model=None)
async def delete_camera_config(camera_id: str) -> dict[str, object] | JSONResponse:
    init_detection_database()
    with sqlite3.connect(detection_database_path()) as connection:
        result = connection.execute(
            "DELETE FROM camera_configs WHERE id = ?",
            (camera_id,),
        )
        if result.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"detail": "Camera configuration not found", "code": "camera_not_found"},
            )
    return {"deleted": camera_id}


@app.post("/api/v1/camera-frame", response_model=None)
async def analyze_camera_frame(
    submission: CameraFrameSubmission,
) -> dict[str, object] | JSONResponse:
    import json
    from datetime import UTC, datetime

    encoded = submission.image_jpeg_base64
    if "," in encoded:
        encoded = encoded.split(",", 1)[1]
    try:
        jpeg = b64decode(encoded, validate=True)
        frame = cv2.imdecode(np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)
    except (ValueError, cv2.error):
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid JPEG camera frame", "code": "invalid_camera_frame"},
        )
    if frame is None:
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid JPEG camera frame", "code": "invalid_camera_frame"},
        )

    detected = detect_people(frame)
    person_count = len(detected)
    record_id = str(uuid4())
    created_at = datetime.now(UTC).isoformat()
    init_detection_database()
    try:
        with sqlite3.connect(detection_database_path()) as connection:
            connection.execute(
                """
                INSERT INTO detections (
                    id, camera_id, detected_at, model_id, model_version,
                    detections_json, person_count, vehicle_count,
                    idempotency_key, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    submission.camera_id,
                    submission.captured_at,
                    "opencv-hog-person",
                    "built-in-default-people-detector",
                    json.dumps([item.model_dump() for item in detected]),
                    person_count,
                    0,
                    submission.idempotency_key,
                    created_at,
                ),
            )
    except sqlite3.IntegrityError:
        existing = next(
            (
                row
                for row in detection_rows()
                if row["idempotency_key"] == submission.idempotency_key
            ),
            None,
        )
        if existing is not None:
            return {"item": existing, "deduplicated": True}

    await manager.broadcast(
        {
            "type": "person_count",
            "camera_id": submission.camera_id,
            "person_count": person_count,
            "detected_at": submission.captured_at,
            "model_id": "opencv-hog-person",
        }
    )
    return {
        "item": {
            "id": record_id,
            "camera_id": submission.camera_id,
            "detected_at": submission.captured_at,
            "model_id": "opencv-hog-person",
            "model_version": "built-in-default-people-detector",
            "detections": [item.model_dump() for item in detected],
            "person_count": person_count,
            "vehicle_count": 0,
            "created_at": created_at,
        },
        "deduplicated": False,
    }


@app.post("/api/v1/detections", response_model=None)
async def record_detections(
    submission: DetectionSubmission,
) -> dict[str, object] | JSONResponse:
    import json
    from datetime import UTC, datetime

    init_detection_database()
    person_count = sum(
        1 for detection in submission.detections if detection.label.lower() == "person"
    )
    vehicle_count = sum(
        1 for detection in submission.detections if "vehicle" in detection.label.lower()
    )
    record_id = str(uuid4())
    created_at = datetime.now(UTC).isoformat()
    try:
        with sqlite3.connect(detection_database_path()) as connection:
            connection.execute(
                """
                INSERT INTO detections (
                    id, camera_id, detected_at, model_id, model_version,
                    detections_json, person_count, vehicle_count,
                    idempotency_key, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    submission.camera_id,
                    submission.detected_at,
                    submission.model_id,
                    submission.model_version,
                    json.dumps([detection.model_dump() for detection in submission.detections]),
                    person_count,
                    vehicle_count,
                    submission.idempotency_key,
                    created_at,
                ),
            )
    except sqlite3.IntegrityError:
        existing = next(
            (
                row
                for row in detection_rows()
                if row["idempotency_key"] == submission.idempotency_key
            ),
            None,
        )
        if existing is None:
            return JSONResponse(
                status_code=409,
                content={"detail": "Detection record conflict", "code": "detection_conflict"},
            )
        return {"item": existing, "deduplicated": True}

    await manager.broadcast(
        {
            "type": "detections",
            "camera_id": submission.camera_id,
            "person_count": person_count,
            "vehicle_count": vehicle_count,
            "detected_at": submission.detected_at,
            "model_id": submission.model_id,
        }
    )
    return {
        "item": {
            "id": record_id,
            "camera_id": submission.camera_id,
            "detected_at": submission.detected_at,
            "model_id": submission.model_id,
            "model_version": submission.model_version,
            "detections": [detection.model_dump() for detection in submission.detections],
            "person_count": person_count,
            "vehicle_count": vehicle_count,
            "created_at": created_at,
        },
        "deduplicated": False,
    }


@app.get("/api/v1/events")
async def events() -> dict[str, list[dict[str, object]]]:
    items: list[dict[str, object]] = [
        {
            "id": "synthetic-event-001",
            "camera_id": "synthetic-camera-001",
            "event_type": "virtual_fence_crossing",
            "confidence": 0.0,
            "created_at": "2026-11-19T08:42:09+05:30",
            "label": "SYNTHETIC",
        }
    ]
    for row in detection_rows():
        detections = row["detections"]
        confidence = max(
            (float(detection["confidence"]) for detection in detections),
            default=0.0,
        )
        person_count = int(row["person_count"])
        vehicle_count = int(row["vehicle_count"])
        items.append(
            {
                "id": str(row["id"]),
                "camera_id": str(row["camera_id"]),
                "event_type": "camera_detection",
                "confidence": confidence,
                "created_at": str(row["detected_at"]),
                "label": f"PERSONS:{person_count};VEHICLES:{vehicle_count}",
            }
        )
    return {"items": items}


@app.get("/api/v1/devices")
async def devices() -> dict[str, list[dict[str, object]]]:
    return {
        "items": [
            {
                "id": "synthetic-device-001",
                "hostname": "demo-edge-node",
                "status": "degraded",
                "software_version": "0.1.0-synthetic",
                "last_seen": "2026-11-19T08:42:09+05:30",
            }
        ]
    }


@app.websocket("/ws/v1/operator")
async def operator_stream(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    sequence = 1
    try:
        while True:
            await asyncio.sleep(5)
            await websocket.send_json(
                {
                    "type": "synthetic_heartbeat",
                    "sequence": sequence,
                    "timestamp": int(time.time()),
                    "label": "TEST DATA",
                }
            )
            sequence += 1
    except WebSocketDisconnect:
        manager.disconnect(websocket)
