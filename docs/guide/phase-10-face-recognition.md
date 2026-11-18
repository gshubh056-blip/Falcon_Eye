# Phase 10 - Face Recognition

## STEP 10.1 – [P1] Detect and align faces
- **Goal:** A face yields a 112x112 aligned image.
- **Implements:** FR-020.
- **Owner / Time:** CV/ML; 75 minutes.
- **Prerequisites:** Privacy review and license approval.
- **Why this step:** Alignment makes recognition consistent across pose.
- **Do this (micro-steps):**
  1. Use approved RetinaFace weights or selectable YOLO face detector.
  2. Extract five landmarks.
  3. Align to 112x112.
- **Expected result:** Face crop and five landmarks are logged.
- **Verify:** `pytest tests/unit/test_face_alignment.py -q`.
- **If it fails:** 80-landmark claim: reject; RetinaFace baseline uses five.
- **Git commit:** `git add apps/frs_service && git commit -m "feat: add five-landmark face alignment"`
- **Done when:** Alignment test passes.

## STEP 10.2 – [P1] Create 512-D embeddings and FAISS
- **Goal:** Face candidates are ranked deterministically.
- **Implements:** FR-021–023.
- **Owner / Time:** CV/ML; 90 minutes.
- **Prerequisites:** Step 10.1 and approved weight.
- **Why this step:** Embeddings allow a watchlist search without storing raw face in every event.
- **Do this (micro-steps):**
  1. Generate L2-normalized 512-D vector.
  2. Build `IndexFlatIP` for demo.
  3. Calibrate threshold with ROC/FAR/FRR.
- **Expected result:** Search ranks only candidates above the configured threshold.
- **Verify:** `python scripts/calibrate_frs.py --dataset datasets/faces/calibration`.
- **If it fails:** Dataset rights unknown: stop. FAR/FRR unavailable: do not deploy.
- **Git commit:** `git add apps/frs_service scripts/calibrate_frs.py && git commit -m "feat: add FAISS face search and threshold calibration"`
- **Done when:** Calibration report and threshold are archived.

## STEP 10.3 – [P1] Enroll governed watchlist faces
- **Goal:** Watchlist items require purpose, approval and expiry.
- **Implements:** FR-024–026.
- **Owner / Time:** Security/Backend; 75 minutes.
- **Prerequisites:** Step 10.2.
- **Why this step:** Face data is high-risk and must be human-governed.
- **Do this (micro-steps):**
  1. Require at least two approved images.
  2. Store legal basis and expiry.
  3. Require supervisor approval.
  4. Log every search actor, purpose and threshold.
- **Expected result:** A match is candidate-only and cannot trigger action autonomously.
- **Verify:** `pytest tests/security/test_face_privacy.py tests/integration/test_face_workflow.py -q`.
- **If it fails:** Missing purpose: 422. Expired watchlist: exclude.
- **Git commit:** `git add apps/frs_service apps/api_gateway && git commit -m "security: add governed face watchlist workflow"`
- **Done when:** Every search leaves an immutable audit record.

## Phase checklist
- [ ] License review pass.
- [ ] Five-landmark alignment pass.
- [ ] FAR/FRR calibration pass.
- [ ] Watchlist and audit pass.
- [ ] Human confirmation is mandatory.

## Phase demo
Use only synthetic or consented faces; show candidate confidence and human review.

## Rollback
Disable FRS service and remove watchlist route from UI.

## Time summary
Phase 10 takes approximately 240 minutes.
