# Phase 05 - Backend API and Dashboard

## STEP 5.1 – [P0 MVP] Create FastAPI settings and app
- **Goal:** A versioned `/api/v1` service runs on port 8000.
- **Implements:** API-001–015, API-025–030.
- **Owner / Time:** Backend/DB; 60 minutes.
- **Prerequisites:** Phase 4 schema and alert/evidence services.
- **Why this step:** FastAPI provides the stable dashboard and C2 integration boundary.
- **Do this (numbered micro-steps):**
  1. Add FastAPI, Uvicorn and HTTPX to requirements.
  2. Create `apps/api_gateway/main.py`:
  ```python
  """FALCON FastAPI application."""
  import structlog
  from fastapi import FastAPI

  logger = structlog.get_logger()
  app = FastAPI(title="FALCON API", version="1.0")

  @app.get("/api/v1/health")
  def health() -> dict:
      logger.info("health_checked")
      return {"status":"ok","mode":"demo"}
  ```
  3. Run:
  ```powershell
  uvicorn apps.api_gateway.main:app --reload --port 8000
  ```
- **Expected result:** Swagger is available at `http://localhost:8000/docs`.
- **Verify:** `curl http://localhost:8000/api/v1/health` returns `{"status":"ok","mode":"demo"}`.
- **If it fails:** Port in use: choose 8010 temporarily and update later. App module missing: set project root and run from root.
- **Git commit:** `git add apps/api_gateway && git commit -m "feat: create versioned FastAPI gateway"`
- **Done when:** Health endpoint and Swagger load.

## STEP 5.2 – [P0 MVP] Implement JWT login and RBAC
- **Goal:** P0 APIs reject anonymous and unauthorized users.
- **Implements:** SEC-001–003, API-001, API-002.
- **Owner / Time:** Security/Backend; 90 minutes.
- **Prerequisites:** Step 5.1.
- **Why this step:** Operators, admins and analysts need different permissions.
- **Do this (micro-steps):**
  1. Create password hashing and login endpoint.
  2. Issue 15-minute JWT access tokens.
  3. Create dependencies for `operator`, `supervisor`, `analyst`, `admin`, `ml`, `auditor`.
  4. Return 401 without token and 403 for wrong role.
- **Expected result:** Demo login yields token and unauthorized API call is denied.
- **Verify:** `pytest tests/security/test_rbac.py -q`.
- **If it fails:** JWT missing: set `JWT_SECRET`. Argon2 package error: install `argon2-cffi`.
- **Git commit:** `git add apps/api_gateway tests/security && git commit -m "security: add JWT and role authorization"`
- **Done when:** 12 role-negative tests pass.

## STEP 5.3 – [P0 MVP] Implement P0 REST endpoints
- **Goal:** Cameras, zones, events, alerts and health are available by API.
- **Implements:** API-003–015, API-025–030.
- **Owner / Time:** Backend/DB; 150 minutes.
- **Prerequisites:** Step 5.2.
- **Why this step:** The dashboard and C2 systems need the exact REST contract.
- **Do this (micro-steps):**
  1. Create routers in `apps/api_gateway/routers/cameras.py`, `zones.py`, `events.py`, `alerts.py`, `health.py`, `audit.py`.
  2. Implement filters, pagination, RFC 7807 errors and `Idempotency-Key`.
  3. Use SQLAlchemy parameterized queries only.
- **Expected result:** Swagger lists all P0 routes.
- **Verify:** `pytest tests/integration/test_api.py -q`.
- **If it fails:** 422: inspect sample JSON. 500: inspect structured log and request ID.
- **Git commit:** `git add apps/api_gateway tests/integration && git commit -m "feat: implement P0 REST API"`
- **Done when:** Each P0 route passes its integration test.

## STEP 5.4 – [P0 MVP] Implement WebSocket alerts and webhook sender
- **Goal:** The dashboard and C2 receive live alert updates.
- **Implements:** FR-077, API-015.
- **Owner / Time:** Backend/Frontend; 75 minutes.
- **Prerequisites:** Step 5.3.
- **Why this step:** Live alert fan-out closes the pipeline without polling.
- **Do this (micro-steps):**
  1. Implement `/ws/v1/operator`.
  2. Publish `alert.created`, `alert.updated`, `camera.status`, `node.health`.
  3. Add HMAC-SHA256 webhook with five retries.
- **Expected result:** WebSocket receives one live JSON alert.
- **Verify:** `pytest tests/integration/test_websocket.py tests/integration/test_webhook.py -q`.
- **If it fails:** CORS or auth: allow demo origin and pass short-lived token.
- **Git commit:** `git add apps/api_gateway && git commit -m "feat: add WebSocket and webhook alert delivery"`
- **Done when:** Dashboard and test webhook receive the same event ID.

## STEP 5.5 – [P0 MVP] Create React TypeScript dashboard
- **Goal:** Login, live wall, alert inbox, evidence, zones and health are usable.
- **Implements:** UI-001–006.
- **Owner / Time:** Frontend; 180 minutes.
- **Prerequisites:** Step 5.4.
- **Why this step:** Operators need an end-to-end control-room view.
- **Do this (micro-steps):**
  1. Create `apps/dashboard` with Vite React TypeScript.
  2. Add pages `Login`, `LiveWall`, `Alerts`, `Evidence`, `Zones`, `Devices`, `Map`.
  3. Use HLS `<video>` for MediaMTX and WebSocket `/ws/v1/operator`.
- **Expected result:** Dashboard displays local stream and live alerts.
- **Verify:** `npm run build && npm run test`.
- **If it fails:** HLS unsupported: use HLS.js package. CORS: allow local origin.
- **Git commit:** `git add apps/dashboard && git commit -m "feat: create MVP React dashboard"`
- **Done when:** M2 flow can be demonstrated in the browser.

## Phase checklist
- [ ] Health and Swagger work.
- [ ] JWT/RBAC tests pass.
- [ ] P0 REST routes pass.
- [ ] WebSocket and webhook pass.
- [ ] React M2 demo works.

## Phase demo
Show login, live wall, line crossing, alert inbox, evidence clip and integrity status.

## Rollback
Stop React and Uvicorn, restore prior API image/container, and point MediaMTX to the prior demo clip.

## Time summary
Phase 5 takes approximately 555 minutes.
