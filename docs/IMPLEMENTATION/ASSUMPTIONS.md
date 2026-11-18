# Implementation Plan Assumptions

Prepared 2026-11-19. These are planning defaults, not verified project facts. Update this file when the team confirms inputs.

| ID | Assumption / default | Validation owner | Due / evidence |
|---|---|---|---|
| ASM-01 | Team size is 6, available time 20 h/person/week, planning horizon 8 weeks, as requested. Team names and availability are unknown. | Team lead | Confirm before kickoff |
| ASM-02 | Capacity is 6 × 20 × 8 = 960 person-hours gross. Plan estimates are task effort, not elapsed time; use 80% planned utilization (768 h) to reserve integration/review/absence capacity. | Team lead | Recalculate after roster is confirmed |
| ASM-03 | No SIH 2026 finale date or fixed project start date was found in the repository. Week 1 is the kickoff week, not a calendar date. | Team lead | Attach official event schedule |
| ASM-04 | Team ID is intentionally blank and must be filled from the official team registration before final submission. | Team lead | Submission gate |
| ASM-05 | Python 3.12.9 and Node 20 LTS are the reproducible target versions because TRD governs. Local Python 3.14.6 is not treated as compatible proof. | DevOps | F0-02 |
| ASM-06 | PostgreSQL 16 plus the exact compatible TimescaleDB extension, Redis 7.4, Mosquitto 2.0, Docker Compose v2 are TRD targets. Exact patch versions/images must be pinned in lock/manifests. | DevOps | F0-03 |
| ASM-07 | `db/schema.sql` is a baseline bootstrap, not a tested migration. Alembic migrations must be generated/reviewed against an empty disposable database before data is used. | Backend | F1-01 |
| ASM-08 | Use TRD's hyphenated service directories; Python package/module names inside them use underscores. | Backend/DevOps | F0-01 |
| ASM-09 | Frontend remains under `apps/dashboard`; React 18/TypeScript/Vite are targets from project docs. No framework package is currently installed. | Frontend | F0-01 |
| ASM-10 | The first end-to-end demo uses a licensed local video file, a synthetic/fixed camera fixture, person/vehicle model output, one fence, alert, snapshot/clip, and local dashboard. It does not depend on internet or cloud. | CV-ML + Backend + Frontend | M3 |
| ASM-11 | No model weights or datasets are present. Downloading pretrained weights/datasets requires license and checksum review; provide an offline cache and deterministic mock inference for development only. | CV-ML | F0-07 |
| ASM-12 | Use open protocols and formats where possible: RTSP/ONVIF, REST/OpenAPI, WebSocket, MQTT, GeoJSON, ONNX, and documented JSON payloads. Compatibility is bounded by an explicit test matrix. | Backend/DevOps | F10 |
| ASM-13 | Public statistics in the PPT remain third-party claims until the exact publication/report is sourced, checked, and dated. They are never presented as Falcon measurements. | Docs/QA | F15-04 |
| ASM-14 | Accuracy, FPS, latency, bandwidth, and false-positive rates are not assumed. Test protocols and hardware/scene details must accompany results. | QA/CV-ML | F13 |
| ASM-15 | Face matching is disabled in the default demo and is not included in MUST scope unless legal basis, consent/authorization, model license, and privacy review are approved. | Security/privacy owner | F7, F12 |
| ASM-16 | No live border camera, sensitive operational footage, credentials, or government-network access is assumed. Synthetic/public properly licensed data and mock integrations are used until approved assets exist. | Team lead | Continuous |
| ASM-17 | No siren GPIO/relay, GPU/Jetson, Edge TPU, IR/thermal camera, NVR, VMS/C4I test system, offline map tiles, or pilot site is guaranteed. Provide a software/mock fallback and label untested hardware support. | DevOps + QA | F2/F8/F10/F11 |
| ASM-18 | Prototype URL in PPT-47 was checked on 2026-11-19 and returned 404. No behavior is inferred. Reuse starts only after the team supplies a working export/link. | Frontend | F0-06 |
| ASM-19 | No “LUT pipe alignment camera driver” code was found in the workspace. Reuse is conditional on receiving source and confirming license/fit; otherwise use a clean driver interface. | Backend | F0-06 |
| ASM-20 | The requested document set describes both MUST and later/stretch work. The eight-week executable baseline is scoped around a safe demoable vertical slice; optional capability plans remain tracked with honest status rather than represented as complete. | Product owner | Kickoff |
| ASM-21 | The assignment/test matrix may refer to a test ID that will be created during implementation; a test is not considered passing until an automated result or signed manual evidence exists. | QA | Continuous |
| ASM-22 | “Offline-safe” means local development/test/operation has a documented path without internet at runtime. Initial package/model/map acquisition may require a separately documented, checksummed staging process. | DevOps | F0-03/F11 |
| ASM-23 | There is no legal or procurement approval in the workspace. Compliance, ministry-policy, PPP, procurement, and C2/C4I alignment are review checklists only, not claims of approval or compliance. | Team lead / legal reviewer | F14 |
| ASM-24 | Capacity estimates are coarse planning ranges converted to point estimates for CSV import. Re-estimate after the first two milestones; preserve the ≤8-hour task size by splitting work. | Team lead | Weekly planning |
