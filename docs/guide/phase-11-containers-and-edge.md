# Phase 11 - Containers and Edge Deployment

## STEP 11.1 – [P0 MVP] Add service Dockerfiles
- **Goal:** Core services build as repeatable non-root containers.
- **Implements:** OPS-001, TRD Section 15.
- **Owner / Time:** DevOps; 120 minutes.
- **Prerequisites:** MVP services pass.
- **Why this step:** Docker makes setup identical across laptop and edge node.
- **Do this (micro-steps):**
  1. Create a Dockerfile for API gateway and capture node.
  2. Pin base `python:3.12-slim`.
  3. Create non-root user and set `read_only` where practical.
- **Expected result:** Images build and list no critical secret.
- **Verify:** `docker build -t falcon/api:local apps/api_gateway`.
- **If it fails:** apt package missing: add build-essential only in builder stage.
- **Git commit:** `git add apps/*/Dockerfile && git commit -m "infra: add core service Dockerfiles"`
- **Done when:** API image starts and `/health` passes.

## STEP 11.2 – [P0 MVP] Add Compose profiles
- **Goal:** Demo, edge and HQ deployments use explicit Compose profiles.
- **Implements:** TRD Sections 4 and 11.
- **Owner / Time:** DevOps; 90 minutes.
- **Prerequisites:** Step 11.1.
- **Why this step:** Profiles stop optional HQ and GPU services from starting on a CPU demo node.
- **Do this (micro-steps):**
  1. Add demo profile for API/dashboard/MediaMTX.
  2. Add edge profile for capture, inference, alert, ledger, sync.
  3. Add hq profile for API, dashboard and central storage.
- **Expected result:** `docker compose --profile demo up` starts only demo dependencies.
- **Verify:** `docker compose --profile demo config`.
- **If it fails:** Profile unknown: update Docker Compose to v2.
- **Git commit:** `git add deploy/docker-compose && git commit -m "infra: add demo edge and HQ Compose profiles"`
- **Done when:** Three profiles resolve to the intended services.

## STEP 11.3 – [P0 MVP] Add systemd watchdog units
- **Goal:** Core service restarts after crash or reboot.
- **Implements:** NFR-013.
- **Owner / Time:** DevOps; 60 minutes.
- **Prerequisites:** Linux edge target.
- **Why this step:** systemd provides unattended restart for border edge nodes.
- **Do this (micro-steps):**
  1. Create `deploy/systemd/falcon-edge.service`.
  2. Set `Restart=always` and `RestartSec=10`.
  3. Enable the service.
- **Expected result:** Process restarts within 10 seconds after SIGKILL.
- **Verify:** `systemctl status falcon-edge && systemctl is-enabled falcon-edge`.
- **If it fails:** Permission denied: run `sudo`; unit typo: `systemd-analyze verify`.
- **Git commit:** `git add deploy/systemd && git commit -m "infra: add systemd edge watchdog"`
- **Done when:** Kill/restart test passes.

## STEP 11.4 – [P0 MVP] Implement sync outbox and inbox
- **Goal:** Offline events and evidence sync without duplicates.
- **Implements:** TR-SYNC-001, DB-003.
- **Owner / Time:** Backend/DevOps; 120 minutes.
- **Prerequisites:** Alert and event IDs are stable.
- **Why this step:** Store-and-forward keeps core events available through network loss.
- **Do this (micro-steps):**
  1. Persist `idempotency_key`, sequence and payload in `sync_queue`.
  2. Retry 5, 10, 20 seconds up to 300 seconds.
  3. Upload metadata separately from object evidence.
- **Expected result:** 100 replayed events yield exactly 100 central events.
- **Verify:** `pytest tests/integration/test_sync.py -q`.
- **If it fails:** Duplicate event: enforce unique idempotency key. Lost order: sequence per camera.
- **Git commit:** `git add apps/sync_service tests/integration/test_sync.py && git commit -m "feat: add offline sync outbox"`
- **Done when:** M4 disconnect/resync test passes.

## STEP 11.5 – [P2 optional] Export ONNX and benchmark hardware
- **Goal:** Optional TensorRT/OpenVINO exports preserve schemas.
- **Implements:** TST-004, NFR-001.
- **Owner / Time:** CV/ML; 180 minutes.
- **Prerequisites:** P0 GPU/edge hardware and benchmark dataset.
- **Why this step:** GPU acceleration is not guaranteed until benchmarked.
- **Do this (micro-steps):**
  1. Export FP16 and INT8 ONNX.
  2. Build TensorRT engine on NVIDIA only.
  3. Export OpenVINO on Intel only.
  4. Run stream benchmark and save report.
- **Expected result:** Engine meets target only on measured hardware.
- **Verify:** `python scripts/benchmark.py --hardware-profile jetson-orin`.
- **If it fails:** Engine mismatch: rebuild for exact GPU/driver. Accuracy drop: do not promote INT8.
- **Git commit:** `git add models/exports models/benchmarks && git commit -m "perf: add optional hardware export benchmark"`
- **Done when:** Report identifies hardware and target status.

## Phase checklist
- [ ] Core images build.
- [ ] Compose profiles work.
- [ ] systemd restarts the service.
- [ ] Offline sync passes.
- [ ] GPU exports are optional.

## Phase demo
Show one container stack, disconnect HQ, queue a local event, restore, and show no duplicate.

## Rollback
Use Compose demo profile and disable sync/hardware workers.

## Time summary
Phase 11 takes approximately 570 minutes.
