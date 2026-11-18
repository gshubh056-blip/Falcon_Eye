# Developer Environment Runbook

**Status:** target runbook for implementation; most commands are not runnable until Phase 0 creates manifests, Makefile, services and Compose. Do not treat this file as proof a backend exists.

## Clean-machine prerequisites

| Requirement | Target | Verification |
|---|---|---|
| OS | Windows 11 with WSL2 Ubuntu 24.04, or Ubuntu 24.04 LTS | `wsl --status` or `lsb_release -a` |
| Git | Current supported version | `git --version` |
| Python | 3.12.9 (TRD) | `python --version` |
| Python package manager | uv pinned in project toolchain | `uv --version` |
| Node | 20 LTS | `node --version` |
| Package manager | npm bundled with pinned Node; lockfile committed | `npm --version` |
| Containers | Docker Engine/Desktop with Compose v2 | `docker version`; `docker compose version` |
| Optional inference hardware | NVIDIA GPU/Jetson with compatible driver/TensorRT, or CPU | `nvidia-smi` where supported; record model/device |
| Storage | Space for images, DB, model cache, test clips and evidence | Check disk budget in F14-03 |
| Network | Initial install/package/model acquisition only; runtime demo must be offline-capable | Run offline acceptance procedure |

Never copy production camera credentials into `.env`. Use a local secret manager, Docker secrets, or an untracked development env file. `.env.example` contains names and safe dummy values only.

## Expected first-time setup (after F0)

From the repository root in a PowerShell or WSL shell:

```powershell
git clone <approved-repository-url> falcon
Set-Location falcon
python --version
node --version
docker compose version
uv sync --frozen
Set-Location apps\dashboard
npm ci
Set-Location ..\..
Copy-Item .env.example .env
```

Replace `<approved-repository-url>` only after the team creates a repository. The workspace inspected on 2026-11-19 is not a Git repository; the clone command is therefore a future setup step.

## Expected Make targets

Implement and document these targets in F0/F15. If a target is missing, report that Phase 0 is incomplete; do not silently substitute a different workflow.

| Command | Expected result |
|---|---|
| `make setup` | Check pinned tools, install locked Python/Node dependencies, create local directories, validate env names |
| `make lint` | Run Python/TS lint and formatting checks |
| `make typecheck` | Run mypy/TypeScript checks |
| `make test` | Run unit and contract suites; integration tests state which services are required |
| `make dev` | Start local services with health checks and hot reload |
| `make demo` | Start offline-capable synthetic demo; inject a clearly labeled event |
| `make down` | Stop local Compose services without deleting persistent data |
| `make clean-test-data` | Remove only explicitly named disposable test volumes after confirmation |
| `make benchmark` | Run selected benchmark with metadata; no default claim output without hardware/data |

## Service run modes

1. **Unit-only:** tests and synthetic fixtures; no DB, camera, broker, model weights, or network.
2. **Local integration:** Compose PostgreSQL/TimescaleDB, Redis/MQTT, MinIO and services; seed synthetic records.
3. **Offline demo:** preloaded model/video/tiles/container images, local database/broker/storage, local web UI; external egress blocked.
4. **Hardware validation:** named camera/NVR, selected edge compute, GPU driver, optional relay/IR sensor; isolated and authorized lab only.

## Port reference

Ports are TRD planning defaults; confirm actual Compose bindings before using them. Bind sensitive services to localhost or a private interface; do not expose them to the Internet.

| Service | Port | Purpose |
|---|---:|---|
| FastAPI REST/WebSocket | 8000 | `/api/v1` and `/ws/v1/operator` |
| Dashboard dev server | 5173 | Local Vite development |
| PostgreSQL/TimescaleDB | 5432 | Local persistence |
| Redis | 6379 | Optional queue/pub-sub |
| Mosquitto MQTT | 1883 | Optional edge alert fan-out |
| MinIO API / Console | 9000 / 9001 | Local evidence object storage |
| MediaMTX RTSP / HLS / WebRTC | 8554 / 8888 / 8889 | Local stream delivery if configured |
| Prometheus / Grafana | 9090 / 3000 | Optional monitoring profile |

## Verification commands expected after scaffolding

```powershell
uv run pytest tests\unit
uv run pytest tests\integration
Set-Location apps\dashboard
npm test -- --run
npm run build
Set-Location ..\..
docker compose config
docker compose ps
```

These are planned command shapes, not a record of successful runs. F0 must make test selectors consistent with the final lockfiles and Makefile. PostgreSQL schema validation must use a clean disposable database, not the user’s operational data.

## Offline exercise

1. Stage signed/pinned package caches, images, model weights, video, and tile pack; verify SHA-256 against manifests.
2. Start the offline profile and verify health on localhost.
3. Disable external network access; confirm local video, inference path, alert, snapshot/clip, UI and evidence verification still work.
4. Generate a local outbox event; verify it is pending and idempotent.
5. Restore only the local mock central link; confirm ordered sync and no duplicate.
6. Document every component that failed to start without network. Do not label the system fully offline until all P0 functions pass.

## Troubleshooting

| Symptom | Checks | Safe response |
|---|---|---|
| `uv sync`/`npm ci` fails | Match pinned Python/Node; verify lockfile and package cache; record exact error | Do not upgrade dependencies ad hoc; create a reviewed lock update |
| Timescale extension missing | Check image/version and `CREATE EXTENSION` permissions | Stop migrations; use pinned Compose DB; never fall back to plain PostgreSQL silently |
| RTSP auth/timeout | Verify URL, credentials reference, network route, codec and clock; inspect redacted structured logs | Rotate credentials if exposed; use local file driver while debugging |
| No camera frames | Check decode pipeline, source type, heartbeat and queue metrics | Show degraded state; never report “live” using stale frames |
| GPU/model load fails | Verify artifact checksum/license/runtime/driver | CPU/smaller model or explicit disabled state; do not load unverified weights |
| WebSocket stale | Inspect heartbeat, sequence gap and REST resync result | Show stale banner and last update; avoid aggressive polling |
| Evidence write fails | Check object-store health, permissions, disk, encryption key reference | Preserve event metadata and surface evidence failure; never report evidence saved |
| Demo appears offline | Check local-only service health before network; confirm no hosted auth/tile dependency | Use offline mock; label fallback and keep evidence visible |
| Secret appears in log/Git | Stop demo, rotate/revoke secret, preserve incident evidence and audit | Remove through approved secret-remediation process; do not rewrite history destructively |

