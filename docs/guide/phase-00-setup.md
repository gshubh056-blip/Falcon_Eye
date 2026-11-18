# Phase 00 - Setup

## STEP 0.1 – [P0 MVP] Install Git and create the repository
- **Goal:** A tracked FALCON repository exists with protected branches and a clean ignore policy.
- **Implements:** TRD Sections 3 and 16.
- **Owner / Time:** DevOps/Security; 45 minutes.
- **Prerequisites:** GitHub account and VS Code.
- **Why this step:** Git records every step and prevents one student from silently overwriting another student's work.
- **Do this (numbered micro-steps):**
  1. Install Git on Windows and verify:
  ```powershell
  git --version
  ```
  ```bash
  git --version
  ```
  2. Open PowerShell and enter the workspace:
  ```powershell
  cd C:\Users\<user>\OneDrive\Pictures\OneDrive\Desktop\Falcon_Eye
  ```
  3. Initialize and select the main branch:
  ```powershell
  git init
  git switch -c main
  ```
  4. Create the GitHub repository named `falcon-eye`.
  5. Add the origin and push:
  ```powershell
  git remote add origin https://github.com/<org>/falcon-eye.git
  git add .gitignore docs/PRD.md docs/TRD.md
  git commit -m "docs: establish PRD and TRD"
  git push -u origin main
  ```
- **Expected result:** GitHub displays `main` with the PRD and TRD.
- **Verify (must pass before continuing):**
  ```powershell
  git status
  git remote -v
  ```
- **If it fails:** `git is not recognized`: install Git and reopen VS Code. `src refspec main does not match`: make an initial commit. `permission denied`: verify GitHub authentication.
- **Git commit:** `git add docs/PRD.md docs/TRD.md .gitignore && git commit -m "docs: establish PRD and TRD"`
- **Done when:** `main` is pushed and teammates can clone the repository.

## STEP 0.2 – [P0 MVP] Install Python 3.12 and Node 20 LTS
- **Goal:** One Python and Node toolchain is available for every member.
- **Implements:** TRD Section 2.
- **Owner / Time:** All members; 30 minutes.
- **Prerequisites:** Administrator access.
- **Why this step:** A fixed language baseline avoids package and lock-file differences.
- **Do this (numbered micro-steps):**
  1. Install Python 3.12.9 from python.org on Windows or `pyenv`/package manager on Ubuntu.
  2. Verify:
  ```powershell
  py -3.12 --version
  node --version
  npm --version
  ```
  ```bash
  python3.12 --version
  node --version
  npm --version
  ```
  3. Install Node 20 LTS from the official Node installer or `nvm`.
- **Expected result:** Python is 3.12.x and Node major is 20.
- **Verify (must pass before continuing):**
  ```powershell
  py -3.12 -c "import sys; print(sys.version)"
  node --version
  ```
- **If it fails:** `py` cannot find 3.12: add Python to PATH. Node 22 instead of 20: install Node 20 with `nvm use 20`. `npm permission denied`: do not use elevated mode for project npm installs.
- **Git commit:** `git commit --allow-empty -m "chore: document baseline runtimes"`
- **Done when:** Both runtimes report the expected major versions.

## STEP 0.3 – [P0 MVP] Create all TRD folders
- **Goal:** The monorepo structure exists before code is added.
- **Implements:** TRD Section 3.
- **Owner / Time:** Backend/DB owner; 25 minutes.
- **Prerequisites:** Step 0.1.
- **Why this step:** A stable folder contract prevents imports and Docker build paths from drifting.
- **Do this (numbered micro-steps):**
  1. Create folders from PowerShell:
  ```powershell
  $folders = @(
    "apps/capture-node","apps/preprocessor","apps/inference-service","apps/tracker",
    "apps/anpr-service","apps/frs-service","apps/rule-engine","apps/alert-service",
    "apps/event-service","apps/api-gateway","apps/ledger-service","apps/sync-service",
    "apps/dashboard","apps/health-monitor","packages/contracts","packages/evidence",
    "packages/observability","deploy/docker-compose","deploy/kubernetes","deploy/systemd",
    "deploy/edge","models/registry","models/benchmarks","models/exports",
    "datasets/annotation","tests/unit","tests/integration","tests/system",
    "tests/security","tests/performance","scripts","docs/guide"
  )
  foreach ($folder in $folders) { New-Item -ItemType Directory -Force $folder | Out-Null }
  ```
  2. Create README stubs with bash:
  ```bash
  find apps packages deploy models datasets tests -type d -exec sh -c 'test -f "$1/README.md" || printf "# %s\n" "$1" > "$1/README.md"' _ {} \;
  ```
- **Expected result:** `Get-ChildItem apps` and `Get-ChildItem deploy` show the expected folders.
- **Verify (must pass before continuing):**
  ```powershell
  Test-Path apps/capture-node
  Test-Path apps/api-gateway
  Test-Path tests/performance
  ```
- **If it fails:** A folder already exists: `New-Item -Force` is safe. `find` command missing on Windows: run only in WSL/Git Bash.
- **Git commit:** `git add apps packages deploy models datasets tests scripts && git commit -m "chore: create monorepo structure"`
- **Done when:** Every TRD folder exists and has a README where required.

## STEP 0.4 – [P0 MVP] Install Docker Desktop and WSL2
- **Goal:** PostgreSQL, Redis, MQTT, MinIO and MediaMTX run as repeatable containers.
- **Implements:** TRD Sections 4 and 11.
- **Owner / Time:** DevOps/Security; 45 minutes.
- **Prerequisites:** Windows 10/11, virtualization enabled.
- **Why this step:** Containers isolate infrastructure and remove manual database installation differences.
- **Do this (numbered micro-steps):**
  1. Enable WSL2:
  ```powershell
  wsl --install
  wsl --set-default-version 2
  ```
  2. Install Docker Desktop and enable `Use the WSL 2 based engine`.
  3. Restart Docker Desktop.
  4. Verify:
  ```powershell
  docker version
  docker compose version
  ```
- **Expected result:** Both client and server sections appear in `docker version`.
- **Verify (must pass before continuing):**
  ```powershell
  docker run --rm hello-world
  ```
- **If it fails:** `WSL 2 requires update`: run `wsl --update`. `Docker engine stopped`: reopen Docker Desktop and wait 60 seconds. `Hardware assisted virtualization`: enable VT-x/AMD-V in BIOS.
- **Git commit:** `git commit --allow-empty -m "chore: verify Docker Desktop setup"`
- **Done when:** `hello-world` prints that Docker is working.

## STEP 0.5 – [P0 MVP] Create the infrastructure Compose file
- **Goal:** TimescaleDB, Redis, MQTT, and MinIO start with one command.
- **Implements:** TRD Sections 4, 9 and 11.
- **Owner / Time:** Backend/DB owner; 45 minutes.
- **Prerequisites:** Step 0.4.
- **Why this step:** All team members need the same database and broker addresses.
- **Do this (numbered micro-steps):**
  1. Create `deploy/docker-compose/compose.infrastructure.yaml` with complete content:
  ```yaml
  services:
    postgres:
      image: timescale/timescaledb-ha:pg16-latest
      environment:
        POSTGRES_DB: falcon
        POSTGRES_USER: falcon
        POSTGRES_PASSWORD: falcon
      ports: ["5432:5432"]
      volumes: ["falcon-postgres:/home/postgres/pgdata"]
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U falcon -d falcon"]
        interval: 10s
        timeout: 5s
        retries: 12
    redis:
      image: redis:7.4-alpine
      command: redis-server --appendonly yes
      ports: ["6379:6379"]
      volumes: ["falcon-redis:/data"]
    mqtt:
      image: eclipse-mosquitto:2.0
      ports: ["1883:1883"]
      volumes:
        - ./mosquitto.conf:/mosquitto/config/mosquitto.conf:ro
    minio:
      image: minio/minio:latest
      command: server /data --console-address ":9001"
      environment:
        MINIO_ROOT_USER: falconadmin
        MINIO_ROOT_PASSWORD: falcon-secret
      ports: ["9000:9000", "9001:9001"]
      volumes: ["falcon-minio:/data"]
  volumes:
    falcon-postgres:
    falcon-redis:
    falcon-minio:
  ```
  2. Create `deploy/docker-compose/mosquitto.conf`:
  ```text
  listener 1883
  allow_anonymous true
  persistence true
  persistence_location /mosquitto/data/
  ```
  3. Start the stack:
  ```powershell
  cd deploy/docker-compose
  docker compose -f compose.infrastructure.yaml up -d
  docker compose -f compose.infrastructure.yaml ps
  ```
- **Expected result:** Four containers report `Up` or `healthy`.
- **Verify (must pass before continuing):**
  ```powershell
  docker exec falcon-postgres-1 pg_isready -U falcon -d falcon
  docker exec falcon-redis-1 redis-cli ping
  curl http://localhost:9000/minio/health/live
  ```
- **If it fails:** Container name differs: use `docker compose ps -q postgres`. Port in use: stop local PostgreSQL/Redis or change Compose host ports. MinIO HTTP failure: wait 20 seconds and retry.
- **Git commit:** `git add deploy/docker-compose && git commit -m "infra: add local data and message services"`
- **Done when:** PostgreSQL, Redis, MQTT and MinIO are reachable on TRD ports.

## Phase checklist
- [ ] Git and GitHub repository work.
- [ ] Python 3.12 and Node 20 work.
- [ ] All TRD folders exist.
- [ ] Docker/WSL2 is installed.
- [ ] Infrastructure containers are healthy.

## Phase demo
Show `docker compose ps`, a Redis PING, PostgreSQL readiness, MinIO console, and a successful GitHub clone.

## Rollback
Stop infrastructure with `docker compose -f compose.infrastructure.yaml down` and delete only named volumes with `docker volume rm falcon-postgres falcon-redis falcon-minio`.

## Time summary
Setup is approximately 205 minutes for the first team member, with all members sharing runtime verification.
