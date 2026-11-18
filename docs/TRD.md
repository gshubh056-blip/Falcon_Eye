# FALCON Technical Requirements Document

## 1. Purpose and Scope

This TRD translates the FALCON PRD into implementation contracts. It is authoritative for repository layout, versions, ports, protocols, data names, configuration keys, service boundaries, test IDs, and development defaults. When this TRD and `docs/PRD.md` differ, implementation follows this TRD and the conflict is recorded in `docs/guide/00-conflicts.md`.

## 2. Document and System

| Item | Decision |
|---|---|
| Document version | 1.0 |
| Target | Windows 10/11 with WSL2 and Ubuntu 22.04+ |
| Python | 3.12.9 verify compatibility in the environment |
| Node.js | 20 LTS verify exact patch |
| React | 18 |
| FastAPI | Pin a verified release in `requirements.txt`; do not use an unpinned install |
| Database | PostgreSQL 16 + TimescaleDB for PostgreSQL 16 |
| Cache/broker | Redis 7.4 and Eclipse Mosquitto 2.0 |
| Object storage | MinIO latest compatible with S3 API |
| Primary runtime | Docker Compose v2 |
| Edge watchdog | systemd |
| Primary capture | GStreamer 1.x; OpenCV `VideoCapture` fallback |
| Clip encoding | FFmpeg |
| Detector | Ultralytics YOLOv8s baseline; model license review required |
| Tracker | ByteTrack default; DeepSORT optional |
| OCR | PaddleOCR primary; EasyOCR fallback |
| Face | RetinaFace + ArcFace/InsightFace 512-D |
| Vector search | FAISS |
| Dashboard | React/TypeScript |

Python package versions must be resolved once by `pip-compile` and pinned in `requirements.txt`. The guide may mark a package version as “verify before use” only when the team cannot determine compatibility offline.

## 3. Repository Structure

```text
falcon/
  apps/
    capture-node/
    preprocessor/
    inference-service/
    tracker/
    anpr-service/
    frs-service/
    rule-engine/
    alert-service/
    event-service/
    api-gateway/
    ledger-service/
    sync-service/
    dashboard/
    health-monitor/
  packages/
    contracts/
    evidence/
    observability/
  deploy/
    docker-compose/
    kubernetes/
    systemd/
    edge/
  models/
    registry/
    benchmarks/
    exports/
  datasets/
    README.md
    annotation/
  tests/
    unit/
    integration/
    system/
    security/
    performance/
  docs/
    PRD.md
    TRD.md
    guide/
  scripts/
  .github/
    workflows/
    PULL_REQUEST_TEMPLATE.md
  .env.example
  Makefile
```

Every leaf folder must contain `README.md` while empty.

## 4. Ports and Infrastructure

| Component | Port |
|---|---|
| FastAPI API gateway | 8000 |
| React dashboard development server | 5173 |
| WebSocket | `/ws/v1/operator` on 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| MQTT | 1883 |
| MinIO API | 9000 |
| MinIO console | 9001 |
| MediaMTX RTSP | 8554 |
| MediaMTX HLS | 8888 |
| MediaMTX WebRTC | 8889 |
| Prometheus optional | 9090 |
| Grafana optional | 3000 |

## 5. Environment Variables

Create `.env` from `.env.example` for local use. Never commit `.env`.

| Variable | Required | Default/example |
|---|---|---|
| `FALCON_ENV` | Yes | `demo` |
| `FALCON_NODE_ID` | Yes | `edge-node-01` |
| `FALCON_SITE_ID` | Yes | `demo-bop` |
| `DATABASE_URL` | Yes | `postgresql+psycopg://falcon:falcon@localhost:5432/falcon` |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` |
| `MQTT_BROKER` | Yes | `localhost` |
| `MQTT_PORT` | Yes | `1883` |
| `OBJECT_STORE_ENDPOINT` | Yes | `http://localhost:9000` |
| `OBJECT_STORE_ACCESS_KEY` | Yes | `falconadmin` |
| `OBJECT_STORE_SECRET_KEY` | Yes | local-only secret |
| `OBJECT_STORE_BUCKET` | Yes | `falcon-evidence` |
| `JWT_SECRET` | Yes | local-only 32-byte secret |
| `JWT_ISSUER` | Yes | `http://localhost:8000` |
| `JWT_AUDIENCE` | Yes | `falcon-dashboard` |
| `LEDGER_SIGNING_KEY_REF` | P0 | `./keys/edge-private.pem` |
| `RTSP_TRANSPORT` | No | `tcp` |
| `MODEL_DIR` | Yes | `./models/registry` |
| `LOG_LEVEL` | No | `INFO` |

## 6. Configuration Files

All services must read configuration from environment variables and a YAML file. Shared example: `deploy/config/falcon-demo.yaml`.

```yaml
environment: demo
capture:
  transport: tcp
  reconnect_initial_seconds: 2
  reconnect_max_seconds: 30
  reconnect_timeout_seconds: 10
detection:
  model: yolov8s.pt
  input_size: 640
  confidence: 0.40
  nms_iou: 0.55
  analytics_fps: 12
tracking:
  implementation: bytetrack
  confirmation_frames: 3
  lost_track_frames: 30
zones:
  foot_point: bottom_center
  homography_enabled: false
alert:
  cooldown_seconds: 30
  high_escalation_seconds: 60
  critical_escalation_seconds: 30
evidence:
  pre_roll_seconds: 10
  post_roll_seconds: 10
  signed_download_seconds: 900
sync:
  retry_initial_seconds: 5
  retry_max_seconds: 300
```

## 7. Shared Python Contracts

### 7.1 Detection

```json
{
  "schema_version": "1.0",
  "node_id": "edge-node-01",
  "camera_id": "uuid",
  "frame_id": "123456",
  "captured_at": "2026-11-17T10:15:30.123Z",
  "model_id": "detector-yolov8s-001",
  "detections": [
    {"class": "person", "confidence": 0.91, "bbox_xyxy": [120, 200, 180, 420]}
  ]
}
```

### 7.2 Track

```json
{
  "schema_version": "1.0",
  "camera_id": "uuid",
  "track_id": "cam12:482",
  "class": "person",
  "status": "confirmed",
  "ground_point": [150.4, 419.8],
  "timestamp": "2026-11-17T10:15:30.123Z"
}
```

### 7.3 Alert

```json
{
  "schema_version": "1.0",
  "event_id": "uuid",
  "camera_id": "uuid",
  "severity": "high",
  "category": "virtual_fence",
  "title": "Person crossed north line",
  "explanation": {"rule_id": "VFR-1", "direction": "north", "track_id": "cam12:482"},
  "created_at": "2026-11-17T10:15:30.700Z",
  "idempotency_key": "edge-node-01:frame:482:VFR-1",
  "evidence": {"snapshot_id": "uuid", "clip_id": "uuid"}
}
```

## 8. Message and Transport Contracts

| Topic | Producer | Consumer | QoS |
|---|---|---|---|
| `falcon/{site}/camera/{camera_id}/frame_status` | capture-node | health-monitor/dashboard | MQTT 0 |
| `falcon/{site}/camera/{camera_id}/detections` | inference-service | tracker | Redis Stream |
| `falcon/{site}/tracks` | tracker | rule-engine, optional heads | MQTT 1 or Redis Stream |
| `falcon/{site}/alerts/{severity}` | alert-service | dashboard/SOC | MQTT 1 |
| `falcon/{site}/health` | health-monitor | sync/dashboard | MQTT 1 retained |
| `falcon/{site}/config/revision` | api-gateway | edge nodes | MQTT 1 retained |

Redis and MQTT are deployment alternatives for MVP message fan-out. Do not enable duplicate producers for the same event stream.

## 9. Database Contract

Use the exact table names in the PRD:

- `sites`
- `cameras`
- `zones`
- `users`
- `roles`
- `events`
- `detections`
- `tracks`
- `alerts`
- `alert_actions`
- `watchlist_plates`
- `watchlist_faces`
- `face_embeddings`
- `evidence_files`
- `ledger_entries`
- `audit_logs`
- `models`
- `configs`
- `devices`
- `health_metrics`
- `sync_queue`

Alembic is the migration tool. The first migration creates base tables. Timescale hypertables are `events`, `detections`, and `health_metrics`. UUID primary keys use `gen_random_uuid()`.

## 10. API Contract

The API base is `/api/v1`. Authentication is `Authorization: Bearer`. Mutation endpoints accept `Idempotency-Key`. All responses use JSON. Errors use:

```json
{
  "error": {
    "code": "CAMERA_NOT_FOUND",
    "message": "Camera does not exist.",
    "request_id": "uuid",
    "field_errors": []
  }
}
```

Status codes: 200 success, 202 queued, 401 unauthenticated, 403 unauthorized, 404 absent, 409 conflict, 422 invalid input, 429 throttled, 503 unavailable.

Implement all P0 API IDs API-001 to API-015, API-019 to API-022, and API-025 to API-030. P1/P2 expands watchlists and model APIs.

## 11. Evidence and Ledger Contract

Evidence object layout is:

```text
evidence/{site_code}/{camera_id}/{YYYY}/{MM}/{DD}/{event_id}/snapshot.jpg
evidence/{site_code}/{camera_id}/{YYYY}/{MM}/{DD}/{event_id}/clip.mp4
evidence/{site_code}/{camera_id}/{YYYY}/{MM}/{DD}/{event_id}/manifest.json
```

Canonical JSON is sorted keys, UTF-8, no trailing newline. Hash is SHA-256. P0 signatures use Ed25519 in PKCS#8 PEM/private key and SPKI public key. The ledger entry fields are `event_id`, `evidence_sha256`, `metadata_sha256`, `prev_hash`, `entry_hash`, `ed25519_signature`, `signer_node_id`, `merkle_root`, `anchor_status`, `anchored_at`, `created_at`.

## 12. Service Technical Requirements

| TR ID | Requirement |
|---|---|
| TR-ING-001 | Capture uses GStreamer/OpenCV and timestamped monotonic frame IDs. |
| TR-ING-002 | RTSP reconnect starts at 2 seconds and caps at 30 seconds. |
| TR-DET-001 | Detection uses a shared data schema and CPU fallback. |
| TR-DET-002 | YOLO input is 640 or 1280 according config. |
| TR-TRK-001 | ByteTrack is default; confirmation is 3 frames; lost track is 30 frames. |
| TR-FENCE-001 | Zone coordinates are normalized image points. |
| TR-FENCE-002 | Intrusion uses the bottom-centre foot point. |
| TR-ALRT-001 | Alert cooldown default is 30 seconds. |
| TR-EVID-001 | Snapshot and 10-second pre/post clip are generated per event. |
| TR-LED-001 | Evidence is hash chained and Ed25519 signed. |
| TR-SYNC-001 | Sync uses idempotency keys and exponential retry. |
| TR-SEC-001 | JWT tokens expire after 15 minutes. |
| TR-SEC-002 | Privileged login requires MFA. |
| TR-OBS-001 | Structured JSON logs contain request/event/camera/node IDs. |

## 13. Testing Contract

Use pytest for Python, Vitest/React Testing Library for React, Playwright for optional E2E, and k6 or Locust for load tests. Python coverage target is initially 80%; P0 modules target 90%. Test folders follow `tests/unit`, `tests/integration`, `tests/system`, `tests/security`, `tests/performance`.

Golden clips use JSON annotations under `datasets/golden/annotations.json` with fields `clip_id`, `camera_id`, `expected_events`, `license`, `source`, `duration_seconds`, `fps`.

## 14. Performance Contract

MVP CPU path must process at least one 1080p stream at 12 analytics FPS on a supported CPU workstation. Target four streams is a hardware benchmark, not a guarantee. P95 frame-to-alert is 1500 ms. P95 API event search is 2 seconds for 100k event rows.

Optional TensorRT and OpenVINO paths must preserve the same JSON and database schemas.

## 15. Security Contract

- TLS 1.2+; mTLS where services cross trust boundaries.
- AES-256 or encrypted volume for evidence.
- JWT 15-minute access tokens and 24-hour refresh policy.
- Password hashing with Argon2id or bcrypt with per-user salt.
- Minimize facial and plate data.
- Retain audit logs for 7 years as the PRD default.
- Sign Docker images, models, software packages and exports.
- Run containers as non-root with read-only root where practical.

## 16. Branches and Code Quality

Use `main`, `develop`, and `feature/<issue>-<short-name>` branches. Python uses ruff, black, mypy, and pre-commit. Conventional commits use `feat`, `fix`, `docs`, `test`, `chore`, `security`, and `perf`.
