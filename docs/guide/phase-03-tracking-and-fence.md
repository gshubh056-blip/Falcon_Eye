# Phase 03 - Tracking and Virtual Fence

## STEP 3.1 – [P0 MVP] Install ByteTrack
- **Goal:** Detections become persistent track IDs.
- **Implements:** FR-014, TR-TRK-001.
- **Owner / Time:** CV/ML; 45 minutes.
- **Prerequisites:** M0 from Phase 2.
- **Why this step:** A track ID prevents one person crossing a fence repeatedly creating duplicate alerts.
- **Do this (numbered micro-steps):**
  1. Confirm ByteTrack implementation/license is approved.
  2. Create `apps/tracker/byte_tracker.py` with Ultralytics `BYTETracker` or an approved package.
  3. Set confirmation 3 and lost-track 30.
- **Expected result:** Same person remains `track_id=...` across at least 10 frames.
- **Verify (must pass before continuing):**
  ```powershell
  pytest tests/unit/test_tracker.py -q
  ```
- **If it fails:** Track swaps: reduce camera motion or tune confidence. Too many IDs: increase lost-track or reduce NMS threshold.
- **Git commit:** `git add apps/tracker tests/unit/test_tracker.py && git commit -m "feat: integrate ByteTrack with track lifecycle"`
- **Done when:** Unit test confirms one track after three consecutive detections.

## STEP 3.2 – [P0 MVP] Add zone JSON and versioning
- **Goal:** Line and polygon zones have normalized coordinates and versions.
- **Implements:** FR-040, FR-046.
- **Owner / Time:** Backend/DB; 40 minutes.
- **Prerequisites:** Zone table migration after Phase 4 or temporary JSON file.
- **Why this step:** Every alert must explain which exact zone version fired.
- **Do this (numbered micro-steps):**
  1. Create `deploy/config/demo-zone.json`:
  ```json
  {"zone_id":"north-line","camera_id":"demo-camera","type":"line","version":1,"geometry":{"points":[[0.25,0.65],[0.75,0.65]]},"schedule":{"all_day":true},"direction":"both"}
  ```
  2. Validate coordinates from 0 to 1.
- **Expected result:** JSON loads and rejects out-of-range points.
- **Verify:**
  ```powershell
  python -m json.tool deploy/config/demo-zone.json
  pytest tests/unit/test_zone_schema.py -q
  ```
- **If it fails:** Invalid JSON: use `python -m json.tool` to locate line. Wrong normalized range: divide by frame width/height.
- **Git commit:** `git add deploy/config/demo-zone.json && git commit -m "feat: add versioned demo zone"`
- **Done when:** Zone loads and validates.

## STEP 3.3 – [P0 MVP] Implement foot-point collision
- **Goal:** Intrusion uses bottom-centre ground point.
- **Implements:** FR-041, TR-FENCE-002.
- **Owner / Time:** CV/ML; 50 minutes.
- **Prerequisites:** Step 3.1 and 3.2.
- **Why this step:** Bottom-centre stays on the ground plane and is more depth-consistent than box centre.
- **Do this (numbered micro-steps):**
  1. Create `apps/rule_engine/zones.py` with point-in-polygon and line-side functions.
  2. Return `ground_point=(mid_x, y2)`.
  3. Add test vectors for points above, below and on the line.
- **Expected result:** Crossing one side to the other produces a crossing event.
- **Verify:**
  ```powershell
  pytest tests/unit/test_zones.py -q
  ```
- **If it fails:** Line never crosses: check signed side formula. On-line is inconsistent: use epsilon 2 pixels.
- **Git commit:** `git add apps/rule_engine tests/unit/test_zones.py && git commit -m "feat: add bottom-centre zone collision"`
- **Done when:** Unit vectors pass and track crosses are direction-aware.

## STEP 3.4 – [P0 MVP] Draw zones and tracks in OpenCV
- **Goal:** A local viewer lets the team verify tracking visually.
- **Implements:** FR-040, FR-041.
- **Owner / Time:** Frontend/Integration; 60 minutes.
- **Prerequisites:** Steps 3.1–3.3.
- **Why this step:** Visual testing finds wrong coordinate or crossing logic quickly.
- **Do this (numbered micro-steps):**
  1. Create `scripts/zone_viewer.py` using `cv2.imshow`.
  2. Draw green confirmed tracks and yellow line/polygon.
  3. Print event JSON on crossing.
- **Expected result:** A window shows boxes, track IDs, zone and `intrusion` text.
- **Verify:**
  ```powershell
  python scripts/zone_viewer.py --source rtsp://localhost:8554/falcon --zone deploy/config/demo-zone.json
  ```
- **If it fails:** No window in WSL: run under Windows Python or enable VcXsrv. Coordinates wrong: verify normalized conversion.
- **Git commit:** `git add scripts/zone_viewer.py && git commit -m "feat: add virtual fence viewer"`
- **Done when:** M1 video produces at least one intrusion event.

## STEP 3.5 – [P1] Optional DeepSORT fallback
- **Goal:** DeepSORT can be selected from config without changing track output.
- **Implements:** FR-015.
- **Owner / Time:** CV/ML; 60 minutes.
- **Prerequisites:** ByteTrack M1 passed.
- **Why this step:** The TRD allows a configurable fallback for appearance-rich scenes.
- **Do this (numbered micro-steps):**
  1. Add `tracker: bytetrack` to config.
  2. Implement adapter interface `update(detections, frame)`.
  3. Add `tracker: deepsort` switch.
- **Expected result:** Both trackers emit the same Track JSON.
- **Verify:**
  ```powershell
  pytest tests/unit/test_tracker_adapters.py -q
  ```
- **If it fails:** Package license: stop DeepSORT until approved.
- **Git commit:** `git add apps/tracker deploy/config && git commit -m "feat: add optional DeepSORT adapter"`
- **Done when:** Config switch swaps tracker without API or DB schema change.

## Phase checklist
- [ ] ByteTrack confirmation/lost lifecycle works.
- [ ] Zone JSON validates.
- [ ] Bottom-centre collision works.
- [ ] OpenCV viewer shows M1.
- [ ] Optional DeepSORT is not a P0 dependency.

## Phase demo
Play a crossing clip and show the zone, track ID, direction and intrusion event explanation.

## Rollback
Restore `deploy/config/falcon-demo.yaml` tracker to ByteTrack and remove the zone config from active state.

## Time summary
Phase 3 takes approximately 255 minutes.
