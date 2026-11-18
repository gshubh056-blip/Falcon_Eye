# Phase 04 - Database, Alerts and Evidence

## STEP 4.1 – [P0 MVP] Create a Python database migration environment
- **Goal:** PostgreSQL schema is created and versioned with Alembic.
- **Implements:** DB-001, DB-002.
- **Owner / Time:** Backend/DB; 45 minutes.
- **Prerequisites:** Phase 0 infrastructure.
- **Why this step:** Alembic makes a tested schema safe to update on one edge node or across the team.
- **Do this (numbered micro-steps):**
  1. Add `alembic`, `SQLAlchemy`, `psycopg[binary]`, `redis`, `minio`, `boto3`, `python-jose`, `passlib`, `argon2-cffi` to requirements.
  2. Create `apps/api_gateway/alembic.ini`.
  3. Run `alembic init apps/api_gateway/migrations`.
- **Expected result:** An Alembic environment and `versions/` folder exist.
- **Verify:**
  ```powershell
  alembic --help
  ```
- **If it fails:** Alembic no module: pip install in `.venv`. Wrong DB URL: set `DATABASE_URL` from TRD.
- **Git commit:** `git add requirements.txt apps/api_gateway/alembic.ini apps/api_gateway/migrations && git commit -m "feat: initialize database migrations"`
- **Done when:** Alembic CLI runs under the project virtual environment.

## STEP 4.2 – [P0 MVP] Add the first migration
- **Goal:** Every P0 table from the TRD exists in PostgreSQL.
- **Implements:** DB-001, DB-004.
- **Owner / Time:** Backend/DB; 120 minutes.
- **Prerequisites:** Step 4.1.
- **Why this step:** APIs and alert/evidence services cannot run until table contracts exist.
- **Do this (numbered micro-steps):**
  1. Copy the SQL DDL from `docs/PRD.md` Part 6 into SQLAlchemy/Alembic migration functions.
  2. Create hypertables for `events`, `detections`, `health_metrics`.
  3. Add compression and retention policies matching 365/30/24-hour defaults.
- **Expected result:** `alembic upgrade head` completes.
- **Verify:**
  ```powershell
  alembic -c apps/api_gateway/alembic.ini upgrade head
  docker exec falcon-postgres-1 psql -U falcon -d falcon -c "\dt"
  ```
- **If it fails:** Extension missing: verify Timescale image. Migration foreign key order: create parent tables first. Hypertable call fails: call only after table creation.
- **Git commit:** `git add apps/api_gateway/migrations && git commit -m "feat: add FALCON P0 database schema"`
- **Done when:** Every TRD table exists and migration reruns cleanly from zero.

## STEP 4.3 – [P0 MVP] Add Redis Streams and alert dedupe
- **Goal:** One candidate alert becomes one stateful alert with cooldown.
- **Implements:** FR-070–075, TR-ALRT-001.
- **Owner / Time:** Backend/DB; 90 minutes.
- **Prerequisites:** Step 4.2 and Redis container.
- **Why this step:** Deduplication controls alert fatigue.
- **Do this (numbered micro-steps):**
  1. Create `apps/alert_service/engine.py`.
  2. Key dedupe as `camera_id|track_id|rule_id|zone_id`.
  3. Set cooldown 30 seconds.
  4. Implement `new -> acknowledged -> escalated -> resolved -> closed` and false-positive branch.
- **Expected result:** Two repeated events within 30 seconds create one alert.
- **Verify:**
  ```powershell
  pytest tests/unit/test_alert_engine.py tests/integration/test_alert_flow.py -q
  ```
- **If it fails:** Duplicate created: check idempotency key before insert. State invalid: enforce transition table.
- **Git commit:** `git add apps/alert_service && git commit -m "feat: add deduplicated alert state engine"`
- **Done when:** Cooldown and state tests pass.

## STEP 4.4 – [P0 MVP] Create snapshots and pre/post-roll clips
- **Goal:** An alert has annotated snapshot and clip evidence.
- **Implements:** FR-080, FR-081.
- **Owner / Time:** CV/ML and Backend; 90 minutes.
- **Prerequisites:** Step 4.3.
- **Why this step:** Evidence makes an alert reviewable and auditable.
- **Do this (numbered micro-steps):**
  1. Maintain a ring buffer of the latest 10 seconds of frames.
  2. On alert, continue recording 10 seconds.
  3. Call FFmpeg to encode MP4 and save snapshot JPEG.
  4. Write SHA-256 in `evidence_files`.
- **Expected result:** Snapshot exists, clip is 20 seconds or failure reason is precise.
- **Verify:**
  ```powershell
  ffprobe -show_entries format=duration evidence/<event_id>/clip.mp4
  pytest tests/unit/test_evidence.py -q
  ```
- **If it fails:** Clip zero duration: wait post-roll completion before muxing. FFmpeg missing: install and restart shell.
- **Git commit:** `git add apps/event_service scripts && git commit -m "feat: add snapshot and pre-post evidence generation"`
- **Done when:** Alert record has evidence IDs and files have readable duration.

## STEP 4.5 – [P0 MVP] Upload evidence to MinIO
- **Goal:** Evidence follows the TRD object layout and remains retrievable.
- **Implements:** FR-083, FR-085.
- **Owner / Time:** Backend/DB; 60 minutes.
- **Prerequisites:** Step 4.4 and MinIO container.
- **Why this step:** Object storage separates large clips from database rows.
- **Do this (micro-steps):**
  1. Create bucket `falcon-evidence`.
  2. Upload snapshot, clip and manifest to the TRD path.
  3. Store `object_key`, `sha256`, size and encrypted flag.
- **Expected result:** MinIO console lists evidence under the event ID.
- **Verify:**
  ```powershell
  curl http://localhost:9000/minio/health/live
  python scripts/verify_minio_evidence.py --event-id <uuid>
  ```
- **If it fails:** Bucket missing: create it using MinIO console. Credentials reject: use environment values from `.env.example`.
- **Git commit:** `git add apps/event_service scripts/verify_minio_evidence.py && git commit -m "feat: upload and index evidence in MinIO"`
- **Done when:** Every required object resolves under the event ID.

## Phase checklist
- [ ] Migrations run from zero.
- [ ] P0 tables exist.
- [ ] Alert dedupe and state transition pass.
- [ ] Snapshot and clip are generated.
- [ ] Evidence uploads to MinIO.

## Phase demo
Fire an intrusion alert and show DB rows, Redis Stream entry, snapshot, clip and MinIO object.

## Rollback
Run `alembic downgrade base` only on disposable demo data. Stop alert workers and restore snapshot storage from the prior release.

## Time summary
Phase 4 takes approximately 405 minutes.
