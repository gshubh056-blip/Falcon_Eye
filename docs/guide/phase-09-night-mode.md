# Phase 09 - Night and Thermal Mode

## STEP 9.1 – [P1] Implement day/night hysteresis
- **Goal:** Night enhancement activates without flickering.
- **Implements:** FR-060.
- **Owner / Time:** CV/ML; 60 minutes.
- **Prerequisites:** Detection pipeline.
- **Why this step:** A fixed threshold could switch every frame in twilight.
- **Do this (micro-steps):**
  1. Calculate mean luminance or percentiles.
  2. Enter night below 18 and exit above 25.
  3. Allow manual camera override.
- **Expected result:** Night mode remains stable for 5 seconds across threshold.
- **Verify:** `pytest tests/unit/test_night_hysteresis.py -q`.
- **If it fails:** Flicker: widen hysteresis bands.
- **Git commit:** `git add apps/preprocessor tests/unit/test_night_hysteresis.py && git commit -m "feat: add hysteretic night mode"`
- **Done when:** Unit boundary tests pass.

## STEP 9.2 – [P1] Add enhancement chain
- **Goal:** Night/IR frames receive grayscale normalization and denoise.
- **Implements:** FR-061–063.
- **Owner / Time:** CV/ML; 75 minutes.
- **Prerequisites:** Step 9.1.
- **Why this step:** Normalization makes a low-light frame consistent for fine-tuned models.
- **Do this (micro-steps):**
  1. Convert to grayscale only for IR/thermal metadata.
  2. Apply CLAHE within bounded parameters.
  3. Mark fog/rain/glare degradation flag.
- **Expected result:** Night frame is readable and includes degradation metadata.
- **Verify:** `pytest tests/unit/test_preprocessor.py -q`.
- **If it fails:** Night artifacts dominate: reduce CLAHE clip limit.
- **Git commit:** `git add apps/preprocessor && git commit -m "feat: add low-light and thermal preprocessing"`
- **Done when:** Test frames retain reasonable contrast.

## STEP 9.3 – [P1] Fine-tune and evaluate night model
- **Goal:** A licensed night/thermal YOLO variant is benchmarked.
- **Implements:** FR-061, TST-005.
- **Owner / Time:** CV/ML; 180 minutes.
- **Prerequisites:** Approved datasets.
- **Why this step:** Optical model degradation must be measured, not assumed.
- **Do this (micro-steps):**
  1. Prepare FLIR ADAS, LLVIP, KAIST or approved local data.
  2. Run transfer learning with fixed seeds.
  3. Report mAP and recall by day/night/fog.
- **Expected result:** A model card and benchmark JSON exist.
- **Verify:** `python scripts/evaluate_model.py --task detection --dataset datasets/night/test`.
- **If it fails:** Data license unknown: remove set. Thermal false positives: report no deployment result and keep optical fallback.
- **Git commit:** `git add models/benchmarks datasets/annotation && git commit -m "perf: add night and thermal benchmark"`
- **Done when:** No target is presented as achieved until benchmark passes.

## Phase checklist
- [ ] Hysteresis pass.
- [ ] Enhancement pass.
- [ ] Night model report exists.
- [ ] Degradation behavior is visible.

## Phase demo
Show a night clip switching enhancement and a degradation warning on severe glare.

## Rollback
Set camera to `day` override or disable thermal head.

## Time summary
Phase 9 takes approximately 315 minutes.
