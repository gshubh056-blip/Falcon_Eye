# FALCON — Master Implementation Plan

**Project:** Smart India Hackathon 2026 · Team FALCON · Banner “FALCONNN” · PS 26187 · Software · Blockchain & Cybersecurity  
**Team ID:** ____________________ (fill from official registration before submission)  
**Plan baseline:** 2026-11-19 · **Authority:** `docs/PRD.md` > `docs/TRD.md` > `docs/BACKEND_SCHEMA.md` and `db/schema.sql` > `docs/WEB_FLOW.md` > `docs/design/`  
**Status:** Plan only. No application services, frontend router, migrations, tests, Docker stack, or model pipeline are currently implemented. Read [00_SOURCE_INVENTORY.md](./00_SOURCE_INVENTORY.md), [00_CONFLICTS_AND_DECISIONS.md](./00_CONFLICTS_AND_DECISIONS.md), and [ASSUMPTIONS.md](./ASSUMPTIONS.md) before starting.

**Architecture one-liner (target, not current implementation):** `CCTV Feed → FFmpeg → YOLO Detection → ByteTrack Tracking → Face/ANPR Recognition → Behaviour Analytics → Threat Engine → FastAPI Backend → Database Storage → Real-Time Dashboard Alerts`.

## How to execute

1. Use the named output paths and canonical PRD/TRD contracts. Do not silently invent an API, field, screen action, severity, or lifecycle value.
2. Keep every task at **8 hours or less**. Split any task that exceeds its estimate. Update `04_TASK_BOARD.csv` whenever estimates, dependencies, owner, or acceptance evidence changes.
3. Finish the vertical slice first: **licensed local video → person/vehicle detection → track confirmation → virtual-fence crossing → alert → evidence → dashboard → integrity verification**. It must run without Internet.
4. At each phase gate, keep only behavior backed by an API and test. Disable unavailable UI actions; mock events are visibly labeled and never represented as model output.
5. Prioritize P0/MUST scope. P1/SHOULD work follows only when the vertical slice passes. P2/COULD/STRETCH is opt-in. The schedule/cut line is in [03_TIMELINE_AND_MILESTONES.md](./03_TIMELINE_AND_MILESTONES.md).
6. Preserve model, video, and person data licenses; never put camera credentials, secrets, or operational footage in Git.

## Target repository layout

Use the TRD’s hyphenated service directories; Python import packages inside them use underscores. This is a target tree, not current repository state.

```text
apps/
  api-gateway/       # FastAPI REST, auth, RBAC, WebSocket
  capture-node/      # Camera driver, preprocess, bounded frame queues
  inference-worker/  # Detector, tracker, rules, model registry adapters
  alert-worker/      # Alert fan-out, escalation, webhook retry/DLQ
  sync-worker/       # Store-and-forward outbox
  dashboard/         # React 18 + TypeScript + Vite
pipeline/            # Shared contracts and inference/rule adapters
db/                  # schema.sql, Alembic migrations, seeds
deploy/              # Compose, Dockerfiles, systemd, broker/storage config
scripts/ tests/ docs/
```

## Task register

Each task has one accountable owner role; contributors can pair. Inputs name authoritative documents and applicable PPT facts. Estimates are person-hours; acceptance criteria are observable. Full importable rows are in [04_TASK_BOARD.csv](./04_TASK_BOARD.csv).

### Phase 0 — Foundation

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F0-01 | Scaffold the monorepo and documented service boundaries. | DevOps | TRD §repo; PPT-31 | `apps/*`, `pipeline/`, `db/`, `deploy/`, `tests/`, root `README.md`, `CONTRIBUTING.md` | — | 8 | MUST | Clean tree matches TRD names; branch/PR/commit convention is documented; each service has a README and no duplicate `/web` tree. | T0-01 | M | Y; create from checked-in templates |
| F0-02 | Pin runtimes, dependency manifests, base images, formatting, lint, type-check, pre-commit. | DevOps | TRD versions; PPT-31 | `pyproject.toml`, `uv.lock`, `apps/dashboard/package.json`, lockfile, `.pre-commit-config.yaml`, Docker base image pins | F0-01 | 8 | MUST | Clean install on Python 3.12.9/Node 20; pinned tools/base images report versions; format/lint/type-check pass. | T0-02 | M | Y after package cache is staged |
| F0-03 | Add safe config/secrets conventions and CI. | DevOps | PRD security; TRD; PPT-17, PPT-32 | `.env.example`, secret-loading module, `.github/workflows/ci.yml` | F0-02 | 8 | MUST | CI runs lint, unit tests, frontend build, dependency/secret scan; test proves missing required secret fails startup. | T0-03 | H | Y; local CI commands work without hosted services |
| F0-04 | Resolve repository naming, architecture ADR and TRL baseline. | Docs | TRD; `docs/guide/README.md`; PPT-39 | `docs/ARCHITECTURE.md`, `docs/adr/0001-repository-layout.md`, `docs/TRL_ASSESSMENT.md` | F0-01 | 4 | MUST | Paths use TRD hyphenated services; imports documented; current readiness is evidence-based or explicitly “not assessed”; reviewer and target TRL rationale recorded. | T0-04 | M | Y |
| F0-05 | Review the prototype and prior camera-driver pattern. | Frontend | PPT-22, PPT-47; available workspace | `docs/IMPLEMENTATION/PROTOTYPE_REVIEW.md`, driver comparison note | — | 4 | SHOULD | Record prototype fetch as 404 on 2026-11-19 and LUT driver as not found; request replacement artifacts; claim no reuse until inspected. | T0-05 | M | Y; use local screenshots/source if supplied |
| F0-06 | Establish dataset/model license and annotation plan. | CV-ML | PRD/TRD model scope; PPT-32, PPT-39, PPT-43 | `docs/DATASET_AND_ANNOTATION_PLAN.md`, `models_registry/README.md`, Roboflow project checklist, checksum/download script | F0-01 | 8 | MUST | Inventory public/authorized person-vehicle, plate, face, IR/thermal data and Roboflow fence workflow; each source has license, privacy, labels, checksum/cache and approval; block unapproved assets. | T0-06 | H | Partial; prepare manifests offline, acquire approved assets later |

### Phase 1 — Data layer and core API

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F1-01 | Execute and reconcile baseline schema on PostgreSQL 16/TimescaleDB. | Backend | PRD/TRD; `db/schema.sql`; PPT-31 | `db/schema.sql`, `db/validation/` | F0-02 | 8 | MUST | Clean disposable DB applies schema; hypertable keys, indexes, policies and FK behavior are queried and recorded; failures block merge. | T1-01 | H | No DB binary now; use pinned local Compose when available |
| F1-02 | Create Alembic baseline and seed repeatable local data. | Backend | Schema; TRD; PPT-31 | `db/alembic.ini`, `db/migrations/`, `scripts/seed_data.py` | F1-01 | 8 | MUST | Empty DB upgrade and downgrade/restore test succeeds; seed is idempotent and contains synthetic sites/cameras/users only. | T1-02 | M | Y with local DB/container |
| F1-03 | Implement login, refresh, logout, privileged MFA, password hashing and session revocation. | Backend | PRD SEC-002; TR-SEC-001/002; API-001/002; PPT-32 | `apps/api-gateway/app/api/v1/auth.py`, auth service/schemas | F1-02 | 8 | MUST | Access token expires at TRD’s 15-minute default; privileged user cannot enter protected routes before MFA; refresh replay/expiry is rejected and audited. | T1-03 | H | Y; no external identity provider required |
| F1-04 | Enforce PRD role and site-scoped authorization. | Backend | PRD roles; schema; PPT-32 | auth policy service, permission matrix tests | F1-03 | 8 | MUST | Every route has allow/deny tests for Operator, Supervisor, Analyst, Admin, ML Maintainer and Auditor; site boundary denies cross-site reads/writes. | T1-04 | H | Y |
| F1-05 | Implement P0 camera/zone APIs and site-scoped fields. | Backend | PRD FR-001..007, FR-040..046; TRD API-003..010; schema; PPT-24 | `apps/api-gateway/app/api/v1/cameras.py`, `zones.py`, schemas | F1-04 | 8 | MUST | Camera/zone operations match API-003..010; site/group behavior matches FR-007; do not invent separate site/rule routes; OpenAPI contract tests pass. | T1-05 | M | Y |
| F1-06 | Add append-only audit entries and local hash-chain service. | Backend | PRD SEC-006; schema; TR-LED-001; PPT-32 | audit repository/service, `tests/security/test_audit_chain.py` | F1-02, F1-04 | 8 | MUST | Login/config/alert/evidence-access actions record actor, purpose, resource/time; tamper or broken predecessor fails verification. | T1-06 | H | Y |
| F1-07 | Add health/ready, structured logs and Prometheus metrics. | Backend | PRD NFR-012; TR-OBS-001; API-025; PPT-31 | `/health`, `/ready`, `/api/v1/health/nodes`, metrics/log config | F1-02 | 8 | MUST | Readiness reports DB state truthfully; logs correlate request/event/camera/node IDs; dependency failure is degraded, never success. | T1-07 | M | Y |
| F1-08 | Implement user/role admin API and resolve site/rule route gaps. | Backend | PRD API-026/027, FR-007; WEB_FLOW GAP-01..27; PPT-32 | `apps/api-gateway/app/api/v1/{users,roles}.py`, contract decision for sites/rules | F1-04, F1-05 | 8 | MUST | API-026/027 user/role lifecycle passes scoped RBAC tests; site/rule CRUD remains blocked until PRD/TRD contract is approved and documented. | T1-08 | H | Y |

### Phase 2 — Video ingestion

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F2-01 | Define interchangeable camera source/driver and file/phone demo source. | Backend | TRD pipeline; PPT-22, PPT-29 | `apps/capture-node/capture_node/drivers/{base,file,phone}.py` | F0-01 | 8 | MUST | File and optional phone-stream adapters share one timestamped-frame interface; fixtures check shape/time/order; phone source is not required for offline demo. | T2-01 | M | Y; local licensed clips |
| F2-02 | Add RTSP/OpenCV or GStreamer driver and ONVIF discovery/PTZ adapter. | Backend | TRD; PPT-22, PPT-31 | `drivers/{rtsp,onvif}.py`, discovery/PTZ routes | F2-01, F1-05 | 8 | SHOULD | Mocked ONVIF tests cover discovery/auth/PTZ errors; at least one named camera/NVR is tested before claiming compatibility. | T2-02 | H | Partial; recorded fixtures/mock ONVIF when hardware absent |
| F2-03 | Implement reconnect, heartbeat, bounded queues and capture metrics. | Backend | PRD FR-005/006; TR-ING-002; PPT-29, PPT-32 | `capture_node/worker.py`, metrics/status API | F2-01 | 8 | MUST | Drop-oldest queue is bounded; reconnect uses jittered 2–30-second backoff; offline after 10 seconds without decodable frame; recovery after three valid frames; analytics target defaults to 12 FPS. | T2-03 | M | Y |
| F2-04 | Implement resize/denoise/low-light preprocessing and compatibility matrix. | CV-ML | TRD; PPT-22, PPT-27, PPT-29 | `pipeline/preprocess/`, `docs/CAMERA_COMPATIBILITY.md` | F2-01 | 8 | SHOULD | Unit fixtures preserve timestamps/dimensions; documented matrix names codecs, ONVIF profile and tested device or “not tested.” | T2-04 | M | Y; synthetic/image fixtures |

### Phase 3 — Detection and tracking

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F3-01 | Add detector adapter and person/vehicle class-aware filtering. | CV-ML | PRD FR-010..013; TR-DET-001/002; PPT-10, PPT-16, PPT-23, PPT-43 | `pipeline/inference/`, optional `vehicle_type.py`, model config, fixture tests | F2-03, F0-06 | 8 | MUST | Shared schema includes class/confidence/bbox/frame/time/model; ROI <25%, short edge <16px, confidence .40 and NMS IoU .55 defaults are tested; optional vehicle-type classifier is config-gated; animal/shadow fixtures cannot alert; model/license recorded. | T3-01 | H | Y with cached approved weights or clearly labeled mock |
| F3-02 | Add ByteTrack default and DeepSORT adapter switch. | CV-ML | TRD; PPT-23, PPT-32 | `pipeline/tracking/`, config | F3-01 | 8 | MUST | Same fixture produces stable track IDs under selected tracker; switching tracker is config-only; no re-ID claim. | T3-02 | M | Y |
| F3-03 | Add configurable confirmation, trajectory persistence and track tests. | CV-ML | PRD FR-014/017; TR-TRK-001; schema; PPT-23, PPT-43 | tracker persistence service, `tests/pipeline/test_confirmation.py` | F3-02, F1-02 | 8 | MUST | Default three-frame confirmation and 30-lost-frame expiry pass; allowed 2–10-frame override is tested; confirmed ground-point trajectory persists for 300 seconds. | T3-03 | M | Y |
| F3-04 | Add model registry adapter and ONNX/ TensorRT export/benchmark scripts. | CV-ML | TRD; PPT-11, PPT-23, PPT-31 | `models_registry/`, `scripts/export_onnx.py`, `scripts/export_trt.py`, `scripts/benchmark.py` | F3-01 | 8 | SHOULD | Hash/signature checked before load; export records model/hardware/runtime; unsupported GPU path exits with actionable message. | T3-04 | H | ONNX CPU fallback; TensorRT needs compatible GPU |

### Phase 4 — Virtual fence, rule engine and alerts (first demoable vertical slice)

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F4-01 | Implement line/polygon geometry and foot-point crossing. | CV-ML | PRD/TRD; PPT-24, PPT-29 | `pipeline/rules/geometry.py`, geometry tests | F3-03 | 8 | MUST | Known inside/outside/direction cases pass; crossing uses bbox bottom-centre, independent of object depth; invalid/self-intersecting polygons rejected. | T4-01 | M | Y |
| F4-02 | Add fence schedules, allowed classes, direction and calibration versioning. | Backend | Schema; WEB_FLOW fence editor; PPT-24 | zone/rule schemas and service | F4-01, F1-05 | 8 | MUST | Active schedule, direction, class and version are honored; historical event references exact zone version. | T4-02 | M | Y |
| F4-03 | Import Roboflow-style JSON/COCO polygons safely. | Backend | TRD; PPT-24, PPT-31 | `scripts/import_roboflow.py`, `pipeline/rules/importers/` | F4-01 | 6 | SHOULD | Valid fixtures import; malformed, huge, or out-of-range geometry returns field errors without partial writes. | T4-03 | M | Y; no Roboflow account needed |
| F4-04 | Define rule plugin interface and implement fence anomaly event creation. | Backend | PRD pipeline; schema; PPT-21, PPT-29 | `pipeline/rules/base.py`, event service | F4-02, F1-02 | 8 | MUST | Rule emits stable category, explanation, track and zone version; normal activity writes metadata only and does not alert. | T4-04 | M | Y |
| F4-05 | Implement alert dedupe/cooldown, lifecycle, assignment and escalation. | Backend | PRD FR-070..075; TR-ALRT-001; API-014/015; PPT-32 | alert service, `alert_actions` integration | F4-04, F1-04 | 8 | MUST | Tests cover severity enum, 30-second default cooldown, duplicate suppression, valid/invalid transitions, high escalation at 60s, critical at 30s and audit action. | T4-05 | H | Y |
| F4-06 | Push authorized alerts over WebSocket and MQTT/Redis adapter. | Backend | TRD WS; schema; PPT-20, PPT-31 | `apps/api-gateway/app/ws/`, message bus adapter | F4-05 | 8 | MUST | Site-filtered client receives ordered envelope; reconnect sequence gap triggers REST resync; broker may be disabled for local-only mode. | T4-06 | H | Y; in-process adapter for dev, real bus in integration |
| F4-07 | Add HMAC webhook delivery, retry/DLQ and siren abstraction. | Backend | PRD FR-076/077; TRD; PPT-29, PPT-32 | webhook worker/service, `deploy/siren.example.yaml` | F4-05 | 8 | SHOULD | Signature verifies over canonical body; bounded retry/dead-letter passes; siren requires authorized role/approval, 3s timeout and enabled relay; mock fallback is explicit. | T4-07 | H | Y; mock siren and local webhook receiver |
| F4-08 | Capture event snapshot and pre/post evidence clip. | Backend | PRD FR-080/081; TR-EVID-001; schema; PPT-29, PPT-32 | evidence ring buffer/worker, object storage adapter | F4-04, F1-02 | 8 | MUST | Each event stores annotated snapshot and 10-second pre/post clip per TRD or precise failure reason; manifest/checksum saved; storage failure explicit. | T4-08 | H | Y; local encrypted object store |
| F4-09 | Implement event search, geo fields and API response. | Backend | PRD FR-082, API-011/012; schema; PPT-24, PPT-32 | `apps/api-gateway/app/api/v1/events.py`, search indexes | F4-04, F1-05 | 8 | MUST | Camera/time/class/plate/zone/severity/status filters paginate within contract; detail includes explanation and present evidence/coordinates only; no fabricated data. | T4-09 | M | Y |

### Phase 5 — ANPR

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F5-01 | Add plate localization adapter and crop fixtures. | CV-ML | PRD/TRD; PPT-26 | `pipeline/anpr/detect.py`, sample test crops | F3-04 | 8 | SHOULD | Bounding boxes and confidence pass fixture tolerance; no read is emitted below configured quality threshold. | T5-01 | H | Y with cached approved model; otherwise labeled mock |
| F5-02 | Implement perspective correction, segmentation and OCR adapter. | CV-ML | TRD; PPT-26, PPT-31 | `pipeline/anpr/{rectify,segment,ocr}.py` | F5-01 | 8 | SHOULD | PaddleOCR/EasyOCR adapter returns text and per-character confidence; unavailable engine fails explicitly. | T5-02 | H | Y with cached packages/models |
| F5-03 | Implement Indian state-wise format validation and 3–5-frame fusion. | CV-ML | PRD/TRD; PPT-26 | `pipeline/anpr/{validation,fusion}.py` | F5-02 | 8 | SHOULD | Known state-format fixtures pass/reject; fusion reports source-frame count and never hides disagreement. | T5-03 | H | Y |
| F5-04 | Persist reads/watchlist matches and benchmark latency/quality. | Backend | schema; API; PPT-26 | ANPR API/search integration, `docs/ANPR_BENCHMARK.md` | F5-03, F1-05 | 8 | COULD | p50/p95 end-to-end ms and exact-match rate recorded on named hardware/data; <100 ms remains target unless measured. | T5-04 | H | Y; report CPU result if no GPU |

### Phase 6 — Explainable suspicious-activity rules

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F6-01 | Implement loitering and trajectory-toward-fence rule plugins. | CV-ML | PRD FR-050/051; PPT-28, PPT-29 | `pipeline/behaviour/loitering.py`, `toward_fence.py` | F4-04 | 8 | SHOULD | Defaults test 30-second dwell; fence approach defaults 2m for 5s and ≤45° inward vector; explanation includes measured values/threshold/track/rule version. | T6-01 | M | Y |
| F6-02 | Implement speed anomaly and group clustering/movement. | CV-ML | PRD FR-052..054; PPT-28, PPT-32 | `pipeline/behaviour/speed.py`, `group.py` | F3-03 | 8 | COULD | Defaults test 5-second speed smoothing > mean+3 MAD; groups test ≥4 people/5m/10s and ≥3 aligned tracks/>.80/10s; no unvalidated “crowd analytics” claim. | T6-02 | H | Y |
| F6-03 | Implement abandoned-object heuristic with explicit uncertainty. | CV-ML | PRD FR-055; PPT-14, PPT-28 | `pipeline/behaviour/abandoned_object.py` | F3-03 | 8 | COULD | Default stationary duration 300 seconds after owner track expiry; tests cover cancellation; candidate requires operator feedback and states uncertainty. | T6-03 | H | Y |
| F6-04 | Add false-positive feedback export and action-recognition stub. | CV-ML | PRD; schema; PPT-28, PPT-43 | feedback API/export, `pipeline/behaviour/action_recognizer.py`, dataset guide update | F6-01 | 6 | SHOULD | Feedback export is access-controlled and strips disallowed data; crawling/climbing returns “not configured,” never a fake detection. | T6-04 | H | Y; local reviewed export only |

### Phase 7 — Face detection/recognition

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F7-01 | Complete legal basis, model-license and privacy gate before enabling FRS. | Docs | PRD privacy; PPT-25, PPT-32, PPT-39 | `docs/FRS_APPROVAL_CHECKLIST.md` | F0-06 | 6 | MUST (gate) | Named approver, purpose, retention, access, notice/legal basis and model/data licenses documented; absent approval keeps FRS feature flag off. | T7-01 | H | Y |
| F7-02 | Implement face detector/alignment/quality adapter. | CV-ML | PRD FR-020; TRD; PPT-25 | `pipeline/face/detect_align.py` | F7-01 | 8 | COULD | Test face ≥64×64, confidence ≥0.60, five landmarks and 112×112 aligned crop; low quality/occlusion/pose rejected/scored; detection is not identity. | T7-02 | H | Y with approved cached weights |
| F7-03 | Add encrypted embedding store and FAISS index adapter. | CV-ML | PRD FR-021..023; schema; security; PPT-25 | `pipeline/face/index.py`, encrypted storage service | F7-02, F12-02 | 8 | COULD | Embedding is exactly 512 float32 L2-normalized values; cosine ranking and threshold calibration tested; encrypted at rest and absent from logs/API. | T7-03 | H | Y; local encrypted store |
| F7-04 | Implement governed watchlist/match review endpoints and audit. | Backend | PRD RBAC; WEB_FLOW gaps; PPT-25 | feature-gated FRS API, human-review workflow | F7-03, F1-04 | 8 | COULD | Site scope, purpose, expiry, reviewer and audit are tested; threshold match is advisory and never an autonomous enforcement action. | T7-04 | H | Y |

### Phase 8 — Night/IR/thermal

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F8-01 | Implement day/night mode selection with hysteresis and manual override. | CV-ML | PRD FR-060; TRD; PPT-27, PPT-29 | `pipeline/night/mode.py` | F2-04 | 6 | SHOULD | Test <25-lux equivalent or luminance percentile <18 default; schedule/IR override and hysteresis prevent rapid toggling; reason is logged. | T8-01 | M | Y |
| F8-02 | Add model registry selection for visible vs IR/thermal weights. | CV-ML | TRD; PPT-27, PPT-31 | model selector/config, IR fixture metadata | F8-01, F3-04 | 8 | COULD | Selection is deterministic for camera capability and mode; missing IR model falls back explicitly and emits degraded status. | T8-02 | H | Y with cached approved weights |
| F8-03 | Run dawn/dusk/IR/thermal test and publish limitations. | QA | PPT-27, PPT-33, PPT-43 | `docs/NIGHT_THERMAL_EVALUATION.md` | F8-02 | 8 | COULD | Results separate sensor types and conditions; no thermal/IR capability claim without corresponding sensor and footage. | T8-03 | H | Partial; use licensed offline samples if available |

### Phase 9 — Frontend React dashboard and GIS

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F9-01 | Scaffold React app, route shell, tokens, localization and error boundaries. | Frontend | TRD; WEB_FLOW PART 1–2; design docs; PPT-31/32 | `apps/dashboard/src/{app,routes,design}`, package/lock | F0-02 | 8 | MUST | Routes map to WEB_FLOW screen IDs; English/Hindi switch, 403/404/500/offline states, lint/build pass. | T9-01 | M | Y after packages are cached |
| F9-02 | Build login, session expiry, site selection and role-gated navigation. | Frontend | PRD roles; auth API; WEB_FLOW; PPT-32 | auth/site components | F9-01, F1-03 | 8 | MUST | Playwright proves login/logout/expiry and hidden vs forbidden route states for each role; server remains authorization authority. | T9-02 | H | Y |
| F9-03 | Build camera overview/live view with overlays and health. | Frontend | WEB_FLOW live screens; camera/WS API; UI-002; PPT-21, PPT-29 | camera/live pages and overlay client | F9-02, F2-03, F4-06 | 8 | MUST | All loading/degraded/error states; overlay freshness shown; measure ≤2s update on named 16-tile rig or report target not met; no fabricated stream URL. | T9-03 | H | Y; use local file stream |
| F9-04 | Build alert console/detail with acknowledgement, assignment, resolution and escalation. | Frontend | WEB_FLOW alert flow; UI-003; TRD APIs; PPT-32 | alerts pages/actions | F9-02, F4-05, F4-06 | 8 | MUST | Role/action matrix enforced; failed mutation rolls back; severity uses text/icon/color; measured standard task uses ≤4 primary clicks. | T9-04 | H | Y |
| F9-05 | Build event/evidence search, preview, export and integrity verification. | Frontend | WEB_FLOW evidence; PRD FR-083/085; schema/API; PPT-32 | events/evidence pages | F9-04, F4-08, F4-09 | 8 | MUST | Search/pagination shareable; evidence states visible; signed link ≤15min and rechecks authorization; verification links to chain report. | T9-05 | H | Y |
| F9-06 | Build remaining screens: GIS, fence, analytics, devices, models, admin, audit, settings and help. | Frontend | WEB_FLOW SCR-08..25; design screen specs; API gaps; PPT-24, PPT-25, PPT-32 | map/zones/analytics/devices/models/users/audit/settings/help screens, Playwright tests | F9-02, F1-05, F1-08 | 8 | SHOULD | Every WEB_FLOW route SCR-01..25 has a route/state or explicit blocked/read-only contract; offline tile/data fallback and keyboard fence editing work; unsupported FRS/admin actions stay disabled. | T9-06 | H | Y with bundled tiles/fixtures |

### Phase 10 — C2/SOC, VMS and interoperability

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F10-01 | Publish versioned OpenAPI and integration payload contract. | Backend | PRD/TRD; PPT-20, PPT-31, PPT-32 | `docs/API.md`, OpenAPI artifact, contract tests | F1-05, F4-05 | 8 | MUST | Contract includes auth, errors, idempotency, rate limits and examples; breaking change fails snapshot/compatibility test. | T10-01 | M | Y |
| F10-02 | Build mock C2/SOC receiver and signed webhook adapter walkthrough. | Backend | PRD integration; PPT-20 | `tests/integration/c2_receiver/`, docs | F4-07, F10-01 | 8 | SHOULD | Mock verifies signature/replay/idempotency and records delivery; external endpoint is not required. | T10-02 | M | Y |
| F10-03 | Define ONVIF/VMS/C4I adapter boundaries and protocol coverage. | Backend | TRD; PPT-22, PPT-31, PPT-32 | `docs/INTEROPERABILITY_MATRIX.md`, adapter interfaces | F2-02, F10-01 | 8 | COULD | Each protocol/profile marked tested, simulated, unsupported, or pending; no blanket interoperability claim. | T10-03 | H | Y; mock adapters |
| F10-04 | Verify open formats and vendor lock-in escape path. | DevOps | PPT-13, PPT-20, PPT-32 | export/import fixtures for ONNX/GeoJSON/JSONL | F10-01 | 6 | SHOULD | A config, fence and model metadata export/import round-trip passes without vendor account. | T10-04 | M | Y |

### Phase 11 — Offline-first edge deployment and sync

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F11-01 | Implement durable outbox, ordered idempotent sync and resume cursor. | Backend | TRD/schema; PPT-12, PPT-17 | `apps/sync-worker/`, sync API | F1-02, F4-04 | 8 | SHOULD | Retry after interruption creates no duplicate events; per-node order/cursor resumes; conflicts remain visible, not silently overwritten. | T11-01 | H | Y; central endpoint can be local mock |
| F11-02 | Add low-bandwidth priority queue and transfer metrics. | Backend | PRD; PPT-35, PPT-36, PPT-42 | sync priority policy and metrics | F11-01 | 8 | SHOULD | Critical metadata precedes bulk clips; byte counts and quality settings recorded; no claim of reduction until measured. | T11-02 | H | Y |
| F11-03 | Build CPU/smaller-model fallback, watchdog and degraded status. | DevOps | TRD; PPT-34, PPT-39 | worker supervision and degraded-mode tests | F3-04, F11-01 | 8 | SHOULD | Simulated GPU failure keeps capture/API alive on fallback or explicitly reports unavailable mode; restart loop is bounded. | T11-03 | H | Y |
| F11-04 | Package NUC/Jetson Compose profiles and systemd services. | DevOps | TRD deploy; PPT-31, PPT-34 | `deploy/docker-compose.yml`, Dockerfiles, `deploy/systemd/` | F1-02, F2-03, F4-05 | 8 | SHOULD | Compose health checks and systemd restart behavior pass on available host; Jetson profile is not claimed tested absent hardware. | T11-04 | H | Y after images/packages are staged |

### Phase 12 — Security and tamper evidence

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F12-01 | Threat-model APIs, workers, devices, stream inputs and supply chain. | Security | PRD/TRD; PPT-32, PPT-39 | `docs/THREAT_MODEL.md` STRIDE register | F0-04 | 6 | MUST | Each trust boundary has threat, mitigation, owner, test and residual risk; SSRF/RTSP credential leakage included. | T12-01 | H | Y |
| F12-02 | Encrypt evidence/object storage and manage keys outside source. | Backend | PRD/schema; PPT-32, PPT-39 | encryption service, MinIO config, key rotation runbook | F4-04 | 8 | MUST | AES-256 envelope/key reference policy tested; encrypted object cannot be read without authorized key; secrets absent from repo/logs. | T12-02 | H | Y; local key service for dev only |
| F12-03 | Harden TLS, headers, rate limits, CORS, authentication and audit. | Backend | TRD; PPT-32 | middleware/config/security tests | F1-03, F1-04 | 8 | MUST | Negative tests prove TLS policy, secure headers, rate limiting, CORS allowlist and audit for sensitive actions. | T12-03 | H | Y |
| F12-04 | Verify evidence/audit hash chain and signed Merkle ledger blocks. | Backend | schema; `docs/guide/phase-06`; PPT-32 | `/api/v1/evidence/{id}/verify`, chain service, tests | F1-02, F12-02 | 8 | MUST | Tamper, missing predecessor, wrong signature and valid chain cases are distinguished; external chain is optional and disabled by default. | T12-04 | H | Y |
| F12-05 | Add dependency/model artifact provenance and security scan gates. | DevOps | TRD; PPT-31, PPT-32 | pinned SBOM, artifact signature verifier, CI scan | F0-03, F3-04 | 8 | SHOULD | CI fails on unapproved critical dependency/license or altered model artifact; exception is documented with expiry/owner. | T12-05 | M | Partial; offline SBOM scan with staged database |

### Phase 13 — Testing and robustness

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F13-01 | Build unit/integration/API/browser test pyramid and fixtures. | QA | PRD/TRD; all phase contracts; PPT-39/43 | `tests/unit`, `tests/integration`, dashboard Playwright suite | F0-03 | 8 | MUST | CI reports separate suites; deterministic fixtures; core rule/auth/hash code target ≥80% coverage as PRD target, exceptions listed. | T13-01 | M | Y |
| F13-02 | Measure detection precision/recall, alert false positives/negatives and latency. | QA | PPT-11, PPT-33, PPT-43 | `docs/BENCHMARKS.md`, reproducible evaluation script | F3-01, F4-04 | 8 | MUST | Dataset split, label protocol, threshold and confusion matrix recorded; 97%@30FPS shown only side-by-side as external target. | T13-02 | H | Y |
| F13-03 | Measure ANPR, camera-to-dashboard latency, bandwidth, FPS and resource use. | QA | PPT-11, PPT-26, PPT-35 | benchmark report + raw JSON/CSV | F5-04, F9-03, F11-02 | 8 | SHOULD | p50/p95 and hardware/software versions recorded; <100 ms and 70–95% are labeled targets until met reproducibly. | T13-03 | H | Y |
| F13-04 | Run weather/lighting and failure/chaos matrix. | QA | PPT-39, PPT-43 | `tests/robustness/`, `docs/ROBUSTNESS_RESULTS.md` | F8-03, F11-03 | 8 | SHOULD | Rain/fog/glare/night, camera disconnect, network cut, GPU unavailable and DB restart results report recovery time and missed/duplicate alerts. | T13-04 | H | Y; recorded fixtures and injected failures |
| F13-05 | Test feedback-to-dataset export and hot model swap. | QA | PPT-19, PPT-32, PPT-43 | pipeline regression test, retraining procedure | F6-04, F3-04 | 8 | COULD | Labeled false-positive export is reproducible and access-controlled; candidate model is signed, benchmarked and rollback-tested. | T13-05 | H | Y; local review/training only |

### Phase 14 — Pilot, rollout, training and sustainability

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F14-01 | Define PoC/pilot site selection, entry/exit criteria and KPI baseline. | Docs | PRD; PPT-34, PPT-39, PPT-40 | `docs/IMPLEMENTATION/11_PILOT_AND_ROLLOUT_PLAN.md` | F13-02 | 6 | SHOULD | Criteria cover consent/authorization, camera access, connectivity, operators, safety, baseline and rollback; no real deployment assumed. | T14-01 | H | Y; tabletop pilot if no site approval |
| F14-02 | Write operator SOP, training and human-in-loop escalation exercise. | Docs | WEB_FLOW; PPT-40..44 | SOP, training slides/checklist, exercise record | F9-04, F4-05 | 8 | SHOULD | Operator can acknowledge, verify, escalate, mark false positive and retrieve evidence in scenario drill; no automated enforcement. | T14-02 | M | Y |
| F14-03 | Document support, patch/rollback, backup/restore and energy practices. | DevOps | TRD; PPT-39, PPT-44 | maintenance runbook, update/restore test | F11-04, F12-05 | 8 | SHOULD | Restore test meets locally approved RPO/RTO; update rollback tested; energy/cost inputs explicitly marked assumed or measured. | T14-03 | M | Y |
| F14-04 | Complete privacy, regulatory, adoption and change-management review. | Docs | PRD; PPT-39, PPT-44 | review checklist and sign-off fields | F12-01, F14-02 | 6 | MUST (gate) | Named reviewers and unresolved obligations recorded; no legal compliance claim without competent approval. | T14-04 | H | Y |

### Phase 15 — Demo, documentation and submission

| ID | Title / description | Owner | Inputs | Outputs | Depends | h | Priority | Acceptance criteria | Test IDs | Risk | Offline-safe? / alternative |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| F15-01 | Build deterministic `make demo` with synthetic seed and event injection. | DevOps | PRD/TRD demo; PPT-47 | `Makefile`, `scripts/simulate_intrusion.py`, seed data, Compose profile | F11-04, F4-05 | 8 | MUST | One documented command starts local stack and produces a visibly labeled synthetic fence alert/evidence in ≤5 minutes; teardown preserves no secrets. | T15-01 | H | Y |
| F15-02 | Write runbook, architecture, API, troubleshooting and demo story. | Docs | source inventory; UI/backend specs; PPT-30 | `README.md`, `docs/ARCHITECTURE.md`, `docs/API.md`, `docs/DEMO_SCRIPT.md` | F10-01, F15-01 | 8 | MUST | Clean-machine reviewer follows steps; ports/roles/limits match config; architecture contains PPT-30 flow labeled target. | T15-02 | M | Y after caches are staged |
| F15-03 | Run PPT-to-product evidence review and benchmark claim review. | QA | PPT-01..47; benchmarks | `docs/IMPLEMENTATION/10_PPT_COVERAGE_MATRIX.md`, signed evidence references | F13-02, F13-03 | 8 | MUST | Every fact/keyword has status, task, evidence/test and repo location; unsupported numbers remain clearly third-party/target. | T15-03 | H | Y |
| F15-04 | Verify references/market/competitor citations and prototype status. | Docs | PPT-37, PPT-45..47 | `docs/IMPLEMENTATION/14_REFERENCES_AND_COMPETITIVE_ANALYSIS.md`, source log | F0-05 | 8 | SHOULD | Each source has URL/access date/use; inaccessible sources marked unverified; competitor claims attributed, not stated as verified Falcon facts. | T15-04 | M | No; cache lawful copies/citations for offline review |
| F15-05 | Rehearse demo and submit release checklist with offline fallback. | QA | demo script; Team ID placeholder; PPT-01/47 | `docs/IMPLEMENTATION/SUBMISSION_CHECKLIST.md`, backup recording | F15-01..F15-04 | 6 | MUST | Three timed dry runs complete; backup video/build works offline; Team ID, licenses, test evidence, risks, and measured-vs-target slides checked. | T15-05 | H | Y |

## Release gates

- **M0 Foundation:** reproducible toolchain, CI, source/license policy, and agreed paths.
- **M1 API/data:** schema/migration tested on an actual PostgreSQL 16/TimescaleDB instance; auth/RBAC deny-by-default.
- **M2 Capture/inference:** file source and class-aware detector process bounded frames; no external camera required.
- **M3 First demoable vertical slice:** confirmed track crosses versioned fence; persisted alert/evidence appears on local dashboard.
- **M4 Evidence/security:** tamper verification, audit access record, offline operation, and role/site isolation pass.
- **M5 Capability extensions:** ANPR, behavior, FRS and IR are feature-gated and independently measured; no model/accuracy claims without evidence.
- **M6 Submission:** demo rehearsed, all PPT registry rows covered, open risks and Team ID handled.

Do not label the project “production-ready” at M6. A controlled pilot, legal/security review, camera/vendor matrix, model performance evaluation and operational support are separate release decisions.

## First ten tasks to start at kickoff

These are the first task IDs in dependency order. Owners must create the named first artifact/command and then complete the task’s acceptance criteria; filenames are not evidence of completion.

| Order | Task | First exact file or command |
|---:|---|---|
| 1 | F0-01 | PowerShell: `New-Item -ItemType Directory -Force apps\api-gateway,apps\capture-node,apps\inference-worker,apps\alert-worker,apps\sync-worker,apps\dashboard,pipeline,db,deploy,tests,docs\adr` |
| 2 | F0-02 | Create `pyproject.toml` with Python `==3.12.9` toolchain metadata and begin the lockfile |
| 3 | F0-03 | Create `.env.example` containing variable names only; then add CI workflow at `.github\workflows\ci.yml` |
| 4 | F0-04 | Create `docs\adr\0001-repository-layout.md` and record the TRD path decision |
| 5 | F0-05 | Create `docs\IMPLEMENTATION\PROTOTYPE_REVIEW.md`; record the 2026-11-19 404 and request a replacement export/source |
| 6 | F0-06 | Create `docs\DATASET_AND_ANNOTATION_PLAN.md` with source/license/checksum columns before downloading any weights |
| 7 | F1-01 | Create `deploy\docker-compose.yml` with a pinned disposable PostgreSQL 16/TimescaleDB service, then run `docker compose -f deploy\docker-compose.yml up -d postgres` |
| 8 | F1-02 | Create `db\alembic.ini` and baseline migration against the validated disposable schema |
| 9 | F1-03 | Create `apps\api-gateway\app\api\v1\auth.py` using the TRD API-001/002 contract |
| 10 | F1-04 | Create `apps\api-gateway\app\core\authorization.py` and start with deny-by-default role/site tests |

If a prerequisite command fails because the tool is missing, record the blocker and install the pinned toolchain through F0-02; do not skip the task or substitute an unpinned stack.
