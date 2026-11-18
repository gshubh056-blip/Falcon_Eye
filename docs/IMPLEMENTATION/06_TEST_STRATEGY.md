# Test Strategy and Definition of Done

## Test pyramid and tools

| Layer | Tool / location | What it proves | Gate |
|---|---|---|---|
| Static | ruff, mypy, pytest collection, ESLint, TypeScript, dependency/license/SAST scans in CI | Syntax, style, type contracts, dependency policy | Every PR |
| Unit | pytest `tests/unit`; Vitest/Testing Library | Geometry, state machines, validators, permission policy, hashing, reducers, forms | Every PR; deterministic |
| Contract/API | FastAPI TestClient/httpx; OpenAPI snapshot | Request/response fields, status codes, RBAC, idempotency, pagination, errors | Every API change |
| Component | React Testing Library | Loading/empty/error/offline/permission states and accessible semantics | Every UI component |
| Integration | pytest `tests/integration`; disposable PostgreSQL/Timescale, Redis/MQTT, MinIO | DB, worker, broker, evidence, sync boundaries | Before merge/release |
| System/E2E | Playwright; local Compose; synthetic file stream | Login → live → fence → alert → evidence → verify; user workflows | Milestone gates |
| Performance | `scripts/benchmark.py`; k6 or Locust for APIs | FPS, latency, throughput, API latency, resource/bandwidth consumption | Report hardware/config/data |
| Security | pytest negative tests, ZAP/manual threat review, dependency/image scans | Auth/RBAC, SSRF, injection, secrets, signatures, evidence access | Before demo release |
| Robustness | fault injection and repeatable fixtures | Disconnect, process/DB/GPU failure, weather/lighting variation, disk pressure | Before M6 |

Use the TRD’s test directories: `tests/unit`, `tests/integration`, `tests/system`, `tests/security`, and `tests/performance`. Playwright/Cypress and k6/Locust are alternatives; choose one and pin it in F0-02. Do not add a competing toolchain without a decision.

## Capability test cases

| Capability / PRD IDs | Required cases | Pass evidence / task |
|---|---|---|
| Camera FR-001..008 | ONVIF discovery timeout/auth; RTSP good/bad credentials and masked export; heartbeat at 10s; one offline and one recovery after 3 valid frames; jittered 2–30s backoff; PTZ stop ≤500ms when supported; site grouping; P1 coordination separate | T2-01..04; T13-04; named camera compatibility report |
| Detection/tracking FR-010..017 | Person/vehicle schema; confidence default .40; ROI <25%; min short edge 16px; NMS IoU .55; 3-frame confirmation; 30-frame expiration; 300s trajectory; DeepSORT same schema; re-ID candidates human-reviewed only | T3-01..04; T13-02; dataset/model manifest |
| Fence FR-040..046 | Normalized coordinates, line/polygon, bottom-centre, direction, schedules, 4-point homography P1, 10s dwell input, immutable zone version, malformed polygon rejection | T4-01..04; T9-06 |
| Alert FR-070..078 | Severity enum invalid→422; dedupe key; 30s default cooldown; escalation high 60s/critical 30s; valid lifecycle; false-positive reason; broker/WS reconnect sequence; signed webhook; siren permission/3s timeout; handover P1 | T4-05..07; T9-04; T10-02 |
| Evidence FR-080..085 / SEC-006 | Annotated snapshot; 10s pre/post or exact failure reason; link ≤15min and reauthorization; retention/legal hold; export manifest; valid chain vs one-byte tamper/broken link/bad signature | T4-08; T12-02/04; T13-01 |
| ANPR FR-030..035 | Localization/crop; four-point correction to 320×128; char confidence; 3–5 frame fusion; civilian/BH/military allowlist; candidate match review | T5-01..04; T13-03/05 |
| FRS FR-020..026 | 64×64 min, confidence .60, five landmarks/112×112, 512-D normalized embedding, cosine order, FAR/FRR threshold evidence, consent/legal basis, expiry/supervisor approval, candidate-only human review, purpose audit | T7-01..04; feature remains disabled until gate passes |
| Behavior FR-050..057 | 30s loiter; approach defaults 2m/5s/45°; speed 5s smoothing > mean+3 MAD; groups ≥4/5m/10s and ≥3 aligned/>.80/10s; abandoned candidate 300s; false-positive feedback; explicit P2 stubs | T6-01..04 |
| Night FR-060..063 | <25 lux-equivalent or luminance percentile <18; mode hysteresis; camera schedule override; IR/thermal metadata selection; fog/rain/glare degraded flag and review behavior | T8-01..03; T13-04 |
| Sync/offline NFR-006..008/015 | 72h disconnected design/soak when feasible; durable 1000-event queue across reboot; duplicate/out-of-order/partial evidence replay; priority metadata before clip; disk 10% warning/5% safe mode | T11-01..04; T13-04; TST-010 |
| UI-001..006 | MFA; 16-tile delay ≤2s only on measured reference rig; ≤4-click alert path; invalid evidence never green; unsaved zone prompt; 256kbps clips deferred while metadata/snapshots remain accessible | T9-01..06; WEB_FLOW WQA cases |
| Security SEC-001..007 | TLS 1.2+, service mTLS; privileged MFA; negative RBAC 403 with audit; secrets absent; changed artifact rejected; exact prev_hash chain; approved deletion audit | T12-01..05; security report |
| Audit/health API | Audit entry includes actor/purpose/resource/time; chain tamper rejected; `/health` and `/ready` reflect actual DB/service health; structured logs correlate request/event/camera/node IDs | T1-06/07; T12-04 |

## Benchmark protocol

For every result, record date, dataset/source/license, train/validation/test split, camera/site conditions, labels and adjudication, false-positive definition, model file and SHA-256, runtime/library versions, hardware/GPU/driver, resolution/FPS, thresholds, warm-up, sample size, raw results, and reproducibility command.

| Metric | Measurement method | Target/reference (not presumed) |
|---|---|---|
| Detector quality | Held-out labeled frames; precision, recall, per-class confusion matrix and confidence threshold | PPT/PRD published `97% @ 30 FPS` is only a comparison target/reference; report Falcon result separately |
| Tracker/alert quality | Track confirmation and event-level FP/FN; annotate camera-hour and crossing event counts | No unmeasured “50% improvement” claim |
| Pipeline throughput | Sustained 30-minute run and target 4×1080p streams at 12 FPS; CPU/GPU/RAM/temp/drops | TRD NFR-001 is acceptance target on named reference node; prompt’s 30 FPS is not the PRD capture default |
| Frame-to-alert latency | Monotonic capture timestamp to alert API/WebSocket; p50/p95/p99 | PRD NFR-002 p95 ≤1500ms |
| API latency | 100k seeded events, search and detail query p50/p95/p99 | PRD NFR-003 p95 detail ≤500ms; search ≤2s |
| ANPR | Exact normalized plate match and per-character score plus total processing time, p50/p95 | PPT <100ms is target; no claim until measured |
| Bandwidth | Same camera/sample/retention profile, bytes sent for edge-selective vs cloud-only baseline | PPT 70–95% reduction is target; baseline formula required |
| Availability/recovery | Soak duration, planned/unplanned downtime, reconnect recovery samples | PRD NFR-004 99.5% monthly and NFR-005 95% reconnect ≤30s are longer-term targets; short demo cannot prove monthly uptime |
| Power/storage | Power meter or vendor telemetry, bytes per camera-hour, disk watermarks | No value assumed; report device and configuration |

## Dataset and false-positive protocol

1. Use only approved public, synthetic, or consented footage. Record license and provenance in the dataset manifest.
2. Freeze camera/time/site splits before tuning. Do not leak near-identical adjacent frames across train/test.
3. Define event-level ground truth with two reviewers or adjudication for the held-out set. Report disagreement.
4. Report FP per camera-hour, FN per annotated crossing/event, precision/recall, confidence intervals, and performance by lighting/weather/class where sample sizes allow.
5. Include animals, shadows, rain, glare, insects, motion blur, empty scenes, occlusion, distant persons, vehicles and low-light examples.
6. Multi-frame confirmation is evaluated against latency and missed-event tradeoffs; a single good video is not a benchmark.
7. False-positive feedback export is human-reviewed, purpose-limited, redacted per policy, and never automatically re-trains/promotes a model.

## Failure and chaos matrix

| Injection | Expected safe behavior | Evidence |
|---|---|---|
| RTSP disconnect / invalid credentials | Bounded reconnect; masked credential; camera offline after threshold; no worker hang | T2-02/03; T13-04 |
| HQ network removed | Local detection, alerting and evidence continue; pending sync visible | T11-01; NFR-006 evidence |
| Duplicate/out-of-order sync packets | Idempotent event identity; cursor does not skip missing records | T11-01 |
| GPU/model unavailable | CPU/smaller-model fallback or explicit degraded/failed state, never fake positive | T3-04; T11-03 |
| Database restart / power interruption | Recover committed data and outbox; detect partial evidence; no silent success | T1-01; T13-04 |
| Disk at 10% / 5% | Warning then safe mode; legal-hold evidence protected; alerts explain storage failure | T13-04 |
| Invalid/tampered evidence or model | Verification rejects it and adds audit/security event | T12-04/05 |
| Slow dashboard or browser reconnect | WS gap detected; REST resync; bounded history; no duplicate cards | T4-06; T9-03/04 |

## Definition of Done

- **Task:** acceptance criteria pass; focused tests added; lint/type checks pass; API/schema/docs kept in sync; no secrets/weights/license violations; offline alternative documented; review approved.
- **Phase:** dependency tasks done; integrated test/evidence attached; unresolved risks and gaps listed; no mocks described as real behavior.
- **Release/demo:** clean setup instructions work; P0 end-to-end passes; security/privacy gates pass; local offline path demonstrated; metrics are reproducible; PPT claims are sourced/qualified; backup and rollback work.

## Required TRD tests and mapping

| TRD test | Planned implementation/evidence |
|---|---|
| TST-001 geometry, regex, formulas, hash | T4-01, T5-03, T6-01..03, T12-04 |
| TST-002 RTSP→detect→track→alert→evidence→API | T2-01..03, T3-01..03, T4-04..09 |
| TST-003 4-camera 30-minute soak | T13-04; record actual camera count and duration |
| TST-004 latency/FPS/streams/storage/bandwidth | T13-02/03 |
| TST-005 held-out detection/tracking/OCR/face benchmarks | T13-02/03; FRS only after approval |
| TST-006 auth/RBAC/MFA/injection/SSRF/secrets/dependencies | T12-01..05 |
| TST-007 offline/chaos/recovery | T11-01..04, T13-04 |
| TST-008 operator tasks | T9-04, T14-02 and measured usability session |
| TST-009 evidence tamper/chain/signature | T12-04 |
| TST-010 1000-event sync replay | T11-01, T13-04 |

Focused task-level tests T0-01..T15-05 in the task board supplement these contract families. T1-06 and T1-07 specifically cover audit-chain failure and honest readiness/observability; do not mark either passing based solely on schema constraints.

