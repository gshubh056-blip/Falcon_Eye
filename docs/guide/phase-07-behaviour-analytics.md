# Phase 07 - Behaviour Analytics

## STEP 7.1 – [P1] Implement loitering
- **Goal:** A confirmed track inside a zone for 30 seconds produces explainable loitering.
- **Implements:** FR-050.
- **Owner / Time:** CV/ML; 60 minutes.
- **Prerequisites:** Tracking and zones pass M1.
- **Why this step:** Dwell is an auditable early heuristic, not an opaque model.
- **Do this (micro-steps):**
  1. Track `dwell_start` and `dwell_seconds`.
  2. Trigger at 30 seconds.
  3. Explain rule ID, track, zone and threshold.
- **Expected result:** `LOITER-001` fires once and dedupe suppresses repeats.
- **Verify:** `pytest tests/unit/test_loitering.py -q`.
- **If it fails:** Track jitter: require confirmed status and 3 frames.
- **Git commit:** `git add apps/rule_engine tests/unit/test_loitering.py && git commit -m "feat: add loitering rule"`
- **Done when:** 30-second test fires once.

## STEP 7.2 – [P1] Implement fence approach and speed
- **Goal:** Inward approach and speed anomalies become candidate events.
- **Implements:** FR-051, FR-052.
- **Owner / Time:** CV/ML; 75 minutes.
- **Prerequisites:** Step 7.1.
- **Why this step:** Heading and speed add context without temporal action models.
- **Do this (micro-steps):**
  1. Smooth 5-second speed.
  2. Calculate median absolute deviation and threshold 3 MAD.
  3. Calculate angle toward fence and require <=45 degrees.
- **Expected result:** Test vectors fire/hold as configured.
- **Verify:** `pytest tests/unit/test_trajectory_rules.py -q`.
- **If it fails:** Coordinate units differ: use pixels for demo or homography metres for field.
- **Git commit:** `git add apps/rule_engine tests/unit/test_trajectory_rules.py && git commit -m "feat: add approach and speed rules"`
- **Done when:** Every threshold boundary has a passing test.

## STEP 7.3 – [P1] Implement groups and abandoned objects
- **Goal:** Group clustering/movement and stationary-object candidates are explainable.
- **Implements:** FR-053–055.
- **Owner / Time:** CV/ML/Backend; 90 minutes.
- **Prerequisites:** Step 7.2.
- **Why this step:** Group and object rules can cover high-value scenarios while remaining tunable.
- **Do this (micro-steps):**
  1. Cluster tracks at 5 metres or demo pixel equivalent.
  2. Require 4 persons for 10 seconds.
  3. Require cosine heading >0.80 for 3+ tracks.
  4. Create abandoned-object candidate after 300 seconds; require human review.
- **Expected result:** Every rule emits rule ID, evidence and measured threshold.
- **Verify:** `pytest tests/unit/test_group_rules.py tests/unit/test_abandoned_object.py -q`.
- **If it fails:** False clusters: calibrate homography or camera-specific radius.
- **Git commit:** `git add apps/rule_engine tests/unit && git commit -m "feat: add group and abandoned-object heuristics"`
- **Done when:** Unit tests cover positive and negative cases.

## STEP 7.4 – [P2] Add pose-based climb/crawl head stub
- **Goal:** A feature flag provides no-model stubs until a validated pose model exists.
- **Implements:** FR-056.
- **Owner / Time:** CV/ML; 45 minutes.
- **Prerequisites:** P1 phase stable.
- **Why this step:** It proves the modular head contract without shipping speculative accuracy.
- **Do this (micro-steps):**
  1. Add `pose_enabled=false`.
  2. Raise explicit `NotImplementedError` only when enabled.
  3. Document minimum 500 clips per class before phase promotion.
- **Expected result:** MVP never invokes pose without validation.
- **Verify:** `pytest tests/unit/test_optional_heads.py -q`.
- **If it fails:** Pose accidentally runs: default config remains false.
- **Git commit:** `git add deploy/config apps/rule_engine && git commit -m "feat: add disabled pose stretch stub"`
- **Done when:** Optional head is blocked unless explicitly enabled and benchmarked.

## Phase checklist
- [ ] Loitering passes.
- [ ] Approach/speed pass.
- [ ] Group and abandoned tests pass.
- [ ] Pose is disabled by default.

## Phase demo
Show one loitering event and one group movement event with threshold values visible.

## Rollback
Set each rule `enabled=false` and retain detection/tracking.

## Time summary
Phase 7 takes approximately 270 minutes.
