# Phase 08 - ANPR

## STEP 8.1 – [P1] Add plate detector
- **Goal:** A vehicle frame produces a plate quadrilateral.
- **Implements:** FR-030.
- **Owner / Time:** CV/ML; 90 minutes.
- **Prerequisites:** Detection/tracking stable.
- **Why this step:** Plate localization isolates OCR from whole-frame blur.
- **Do this (micro-steps):**
  1. Prepare approved vehicle/plate dataset or public licensed plates.
  2. Fine-tune or use a licensed pretrained YOLO plate detector.
  3. Export to ONNX after license review.
- **Expected result:** Test plate receives a bounding quadrilateral.
- **Verify:** `python scripts/evaluate_plates.py --dataset datasets/plates/test`.
- **If it fails:** Licence: stop and choose approved model. Small plate: use tiling.
- **Git commit:** `git add apps/anpr_service models/registry datasets/README.md && git commit -m "feat: add plate localization"`
- **Done when:** Plate recall and mAP are recorded.

## STEP 8.2 – [P1] Correct perspective and OCR
- **Goal:** OCR receives a normalized 320x128 plate image.
- **Implements:** FR-031, FR-032.
- **Owner / Time:** CV/ML; 75 minutes.
- **Prerequisites:** Step 8.1.
- **Why this step:** Four-point perspective removes rotation and scale distortion.
- **Do this (micro-steps):**
  1. Apply four-point transform.
  2. Run PaddleOCR.
  3. Produce character-level confidence.
- **Expected result:** OCR text and character confidence are returned.
- **Verify:** `pytest tests/unit/test_plate_perspective.py tests/unit/test_ocr.py -q`.
- **If it fails:** OCR gibberish: normalize grayscale and rotate 180 degrees if policy-safe.
- **Git commit:** `git add apps/anpr_service && git commit -m "feat: add plate perspective and PaddleOCR"`
- **Done when:** OCR test exact text passes.

## STEP 8.3 – [P1] Fuse 3–5 frames and validate Indian formats
- **Goal:** One normalized plate has a watchlist match only after temporal fusion.
- **Implements:** FR-033–035.
- **Owner / Time:** CV/ML/Backend; 90 minutes.
- **Prerequisites:** Step 8.2.
- **Why this step:** Temporal voting reduces blur and OCR false matches.
- **Do this (micro-steps):**
  1. Median/ensemble the 3–5 frame text.
  2. Validate civilian, BH, military and temporary patterns.
  3. Exact-match and fuzzy-match watchlist entries.
- **Expected result:** Valid text yields watchlist candidate with confidence.
- **Verify:** `pytest tests/unit/test_indian_plate_patterns.py tests/integration/test_anpr_watchlist.py -q`.
- **If it fails:** Regex rejects valid plate: use deployment jurisdiction allowlist.
- **Git commit:** `git add apps/anpr_service && git commit -m "feat: add temporal ANPR and watchlist matching"`
- **Done when:** Accuracy script and watchlist test pass.

## STEP 8.4 – [P1] Add ANPR API and dashboard view
- **Goal:** Authorized users search plates and verify matches.
- **Implements:** API-016.
- **Owner / Time:** Frontend/Backend; 60 minutes.
- **Prerequisites:** Step 8.3.
- **Why this step:** Operators must see OCR confidence and not treat it as automatic identity.
- **Do this (micro-steps):**
  1. Implement purpose-required plate search.
  2. Add audit entry.
  3. Display plate, confidence and human decision.
- **Expected result:** Plate result requires human confirmation.
- **Verify:** `pytest tests/integration/test_plate_api.py -q`.
- **If it fails:** Missing purpose: return 422 and audit attempt.
- **Git commit:** `git add apps/api_gateway apps/dashboard && git commit -m "feat: add governed ANPR result workflow"`
- **Done when:** ANPR API/UI has human confirmation.

## Phase checklist
- [ ] Plate detector passes.
- [ ] Perspective/OCR passes.
- [ ] Temporal fusion and Indian patterns pass.
- [ ] Watchlist is governed.

## Phase demo
Show a synthetic plate moving in 5 frames and a candidate alert; do not present OCR as definitive.

## Rollback
Disable ANPR head and retain vehicle tracking.

## Time summary
Phase 8 takes approximately 315 minutes.
