# FALCON Implementation Plan — Source Inventory

Inventory prepared 2026-11-19 from the workspace. “FS date” is the observed last-modified date; when no document version/date is stated, it is not inferred. Specifications describe intended behavior and are not proof that code exists.

| Source | Version/date | Summary |
|---|---|---|
| `.gitignore` | FS 2026-11-18 | Ignores Python/Node artifacts, secrets, model/video files, and datasets. No build configuration is present. |
| `docs/PRD.md` | v1.0; dated 2026-11-17 | Product requirements, P0/P1/P2 scope, personas, API/data contracts, security, and UI expectations. Performance claims are targets, not measured results. |
| `docs/TRD.md` | v1.0; FS 2026-11-18 | Technical authority for versions, repo paths, ports, protocols, schemas, API, and tests. Describes a larger target monorepo than currently exists. |
| `docs/WEB_FLOW.md` | v1.0, aligned to PRD/TRD v1.0; FS 2026-11-19 | Proposed dashboard routes, roles, flows, API mappings, tests, and backend gaps. Routes are proposals, not an implemented router. |
| `docs/BACKEND_SCHEMA.md` | FS 2026-11-19 | Backend architecture, data/process contracts, and delivery stages. Says FastAPI, CV workers, deployment, and tests are not implemented. |
| `docs/ERD.md` | FS 2026-11-19 | Entity relationships and Timescale partition-key notes. Explains the event identity/retention bridge. |
| `docs/ASSUMPTIONS.md` | FS 2026-11-19 | Records 14 technical/schema decisions and conflicts. Notes the database schema was not executed in its documented environment. |
| `docs/guide/README.md` | FS 2026-11-19 | Phase guide index, assumptions, dependencies, and milestones. It is an implementation guide, not an implemented app. |
| `docs/guide/00-conflicts.md` | FS 2026-11-19 | Prior conflict resolutions for Python, enums, UUIDs, Timescale keys, and offline sync. |
| `docs/guide/coverage.md` | FS 2026-11-18 | Maps P0 requirement families to guide steps. Coverage means planned verification, not completed code. |
| `docs/guide/glossary-and-troubleshooting.md` | FS 2026-11-18 | Defines project terms and setup/runtime troubleshooting procedures. |
| `docs/guide/phase-00-setup.md` | FS 2026-11-18 | Prescribes Git, runtimes, folders, containers, and infrastructure setup. Steps are not executed. |
| `docs/guide/phase-01-test-media.md` | FS 2026-11-18 | Plans media tooling, licensed clips, MediaMTX, and RTSP testing. Referenced services/dependencies are absent. |
| `docs/guide/phase-02-walking-skeleton.md` | FS 2026-11-18 | Gives example setup, capture, YOLO, timing, and event-write steps. Target application files are absent. |
| `docs/guide/phase-03-tracking-and-fence.md` | FS 2026-11-18 | Plans ByteTrack, zone versioning, foot-point collision, and local preview. Implementation and tests are absent. |
| `docs/guide/phase-04-database-alerts-evidence.md` | FS 2026-11-18 | Plans migrations, alert lifecycle, evidence generation, and MinIO. Services are absent. |
| `docs/guide/phase-05-api-and-dashboard.md` | FS 2026-11-18 | Gives FastAPI, auth/RBAC, REST/WS, and dashboard milestones. API/dashboard sources are absent. |
| `docs/guide/phase-06-evidence-ledger.md` | FS 2026-11-18 | Plans canonical hashing, Ed25519 signatures, chain verification, and later Merkle anchoring. Services are absent. |
| `docs/guide/phase-07-behaviour-analytics.md` | FS 2026-11-18 | Plans explainable behavioral rules. It does not contain implemented analytics. |
| `docs/guide/phase-08-anpr.md` | FS 2026-11-18 | Plans plate detection/OCR/fusion/validation and a governed workflow. ANPR code/API are absent; guide marks it P1. |
| `docs/guide/phase-09-night-mode.md` | FS 2026-11-18 | Plans mode switching, preprocessing, and model benchmarking. Implementation/results are absent. |
| `docs/guide/phase-10-face-recognition.md` | FS 2026-11-18 | Plans embedding/FAISS and governance. FRS is gated on privacy/license approval and is unimplemented. |
| `docs/guide/phase-11-containers-and-edge.md` | FS 2026-11-18 | Plans service containers, Compose, systemd, sync, and optional hardware exports. Deployment files are absent. |
| `docs/guide/phase-12-security-hardening.md` | FS 2026-11-18 | Plans mTLS, secrets, RBAC/MFA, evidence encryption, and scanning. Controls/tests are not present as code. |
| `docs/guide/phase-13-testing-and-benchmarks.md` | FS 2026-11-18 | Defines tests, benchmarks, evaluation, and chaos testing. Suites and results are absent. |
| `docs/guide/phase-14-demo-and-submission.md` | FS 2026-11-18 | Plans seeded demo, rehearsal, fallback, docs, and measured slides. Scripts/assets are absent. |
| `docs/guide/phase-15-stretch-goals.md` | FS 2026-11-18 | Lists re-ID, UAV, external chain, and other optional work as P2/stretch. |
| `docs/design/README.md` | Design system v1.0; FS 2026-11-19 | Design-system index and implementation guidance. Explicitly states no runnable dashboard/package exists. |
| `docs/design/01-brand-and-principles.md` | FS 2026-11-19 | Identity, voice, and control-room UX principles; emphasizes human decisions and offline honesty. |
| `docs/design/02-colour.md` | FS 2026-11-19 | Four palettes, semantic colors, contrast, and color-vision guidance. |
| `docs/design/03-typography.md` | FS 2026-11-19 | Typography scale and Hindi handling; font binaries are not included. |
| `docs/design/04-layout-spacing-elevation.md` | FS 2026-11-19 | Grid, breakpoints, density, surfaces, and z-index. Wall layouts are limited to measured stream capacity. |
| `docs/design/05-iconography-illustration-motion-sound.md` | FS 2026-11-19 | Icon, motion, sound, and illustration conventions; some referenced illustrations are not present. |
| `docs/design/06-components.md` | FS 2026-11-19 | Component anatomy, states, accessibility, and keyboard behavior. It is specification, not component code. |
| `docs/design/07-screens.md` | FS 2026-11-19 | Proposed Login, Live Wall, Alerts, Evidence, Zones, Health, and other screen compositions. |
| `docs/design/08-accessibility-and-quality.md` | FS 2026-11-19 | Accessibility and visual QA gates; component/browser build checks are not yet runnable. |
| `docs/design/DECISIONS.md` | FS 2026-11-19 | Framework-independent tokens, accessibility, asset, and path decisions; rejects a parallel `/web` app. |
| `docs/design/LICENSES.md` | FS 2026-11-19 | Proposed libraries/fonts and licenses. No dependencies are installed and versions need verification. |
| `apps/dashboard/src/design/tokens.css` | FS 2026-11-19 | CSS theme, typography, spacing, motion, and surface tokens. No application imports it. |
| `apps/dashboard/src/design/tokens.ts` | FS 2026-11-19 | TypeScript theme, severity/integrity, and layout tokens. No UI consumes it. |
| `apps/dashboard/public/brand/contour-pattern.svg` | FS 2026-11-19 | Decorative contour pattern asset. |
| `apps/dashboard/public/brand/falcon-mark.svg` | FS 2026-11-19 | Static FALCON mark asset. |
| `apps/dashboard/public/brand/falcon-wordmark.svg` | FS 2026-11-19 | Static wordmark asset; no font binary accompanies it. |
| `apps/dashboard/public/brand/favicon.svg` | FS 2026-11-19 | Static favicon asset. |
| `db/schema.sql` | FS 2026-11-19 | PostgreSQL 16/TimescaleDB baseline DDL with types, tables, indexes, policies, and triggers; execution is unverified. |
| `scripts/check_contrast.py` | FS 2026-11-19 | Dependency-free contrast checker; the only project script found. |

## Workspace status observed

- 46 files were reviewed. No app/service source, migrations, tests, dependency manifests, Docker/Compose, environment example, OpenAPI file, or root README was found.
- No source prototype project or prior “LUT pipe alignment camera driver” implementation was found in the workspace.
- The prototype URL in PPT-47 returned HTTP 404 during this review (2026-11-19); its former behavior cannot be asserted.
- `python scripts\check_contrast.py` passed. Python 3.14.6 and Git were present; Node/npm, Docker, `psql`, pytest, ruff, mypy, black, and pre-commit were not found in the reviewed environment. The workspace is not a Git repository.
- See [00_CONFLICTS_AND_DECISIONS.md](./00_CONFLICTS_AND_DECISIONS.md) and [ASSUMPTIONS.md](./ASSUMPTIONS.md) for impact and resolution.
