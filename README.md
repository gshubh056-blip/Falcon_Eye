# FALCON EYE

FALCON EYE is a Smart India Hackathon 2026 perimeter and border-monitoring
platform. This repository contains the implementation monorepo for capture,
inference, tracking, alerting, synchronization, the dashboard, database, and
deployment assets.

The implementation is currently in the foundation phase. The requirements and
technical authority are documented in:

- [Product Requirements Document](docs/PRD.md)
- [Technical Requirements Document](docs/TRD.md)
- [Master Implementation Plan](docs/IMPLEMENTATION/01_IMPLEMENTATION_PLAN.md)
- [Implementation Guide](docs/guide/README.md)
- [Contribution Guidelines](CONTRIBUTING.md)

## Repository layout

- `apps/api-gateway/` - FastAPI REST, authentication, authorization, and WebSocket APIs
- `apps/capture-node/` - camera/file ingestion and bounded frame delivery
- `apps/inference-worker/` - detection, tracking, and rule adapters
- `apps/alert-worker/` - alert fan-out and delivery retries
- `apps/sync-worker/` - offline store-and-forward synchronization
- `apps/dashboard/` - React 18, TypeScript, and Vite dashboard
- `pipeline/` - shared contracts and inference/rule adapters
- `db/` - schema and database migrations
- `deploy/` - Compose, Docker, systemd, and edge deployment assets
- `tests/` - unit, integration, system, security, and performance tests
- `docs/` - specifications, decisions, guides, and evidence

Do not commit secrets, model weights, datasets, camera credentials, or
operational media. Use the ignore policy in `.gitignore` and `.env.example` for
local configuration names and safe dummy values.

## Local demo install

1. Install Python 3.12.9, Node 20.20.2, and Docker Desktop.
2. Copy `.env.example` to `.env` and keep every secret local.
3. Start the API:

   ```powershell
   uv run uvicorn app.main:app --app-dir apps/api-gateway --host 127.0.0.1 --port 8000
   ```

4. Start the dashboard:

   ```powershell
   npm --prefix apps/dashboard run preview -- --host 127.0.0.1 --port 4173 --strictPort
   ```

5. Open `http://127.0.0.1:4173/#/cameras`, allow the browser camera, and start the preview.

Browser camera, USB camera, phone HTTP stream, and local video file sources are
supported demo paths. RTSP and ONVIF require a tested edge adapter and are
explicitly unavailable until that adapter exists. TensorFlow COCO-SSD runs in
the browser for the demo; it is not a production-approved person/vehicle model
without the license, provenance, benchmark, and model-registry work described
in `docs/DATASET_AND_ANNOTATION_PLAN.md`. Local detection records are stored in
`data/falcon-detections.sqlite3`, which is intentionally excluded from Git.
