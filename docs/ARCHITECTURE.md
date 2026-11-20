# FALCON Architecture

## Current implementation status

This repository is moving from a specification-only foundation toward runnable
components. The database schema and reversible baseline are validated, and a
local API/dashboard vertical slice may use synthetic in-memory data. The
capture node can decode local video, an OpenCV camera device, or a phone HTTP
stream; no named device compatibility or object detection is claimed yet.

## Service boundaries

- `apps/api-gateway`: authenticated REST/WebSocket gateway and configuration boundary.
- `apps/capture-node`: OpenCV-backed frame sources for local video, camera devices, and phone HTTP streams; RTSP/ONVIF support is not implemented.
- `apps/inference-worker`: detector/tracker target; no licensed model is assumed.
- `apps/alert-worker`: alert fan-out and delivery retries.
- `apps/sync-worker`: store-and-forward synchronization.
- `apps/dashboard`: operator-facing React application.
- `pipeline`: shared frame/detection/track/event contracts.
- `db`: PostgreSQL/TimescaleDB baseline and future migrations.
- `deploy`: local and edge deployment manifests.

## MVP data flow

1. The capture node decodes timestamped frames from a selected source.
2. No detector is configured until a model passes the asset/license gate.
3. The synthetic demo producer can still create a clearly labeled alert event.
4. The API gateway and dashboard expose the current synthetic operator slice.
5. Persistence uses the validated PostgreSQL/TimescaleDB migration path.

## Validation gates

- No secret may be committed.
- Camera credentials use references, never raw URLs or passwords.
- Mock responses must be visually and structurally labeled as test data.
- External integrations require named acceptance tests and measured evidence.
