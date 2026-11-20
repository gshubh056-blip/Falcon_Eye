# FALCON EYE

This repository contains the implementation monorepo for capture,
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
