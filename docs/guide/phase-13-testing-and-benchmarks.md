# Phase 13 - Testing and Benchmarks

## STEP 13.1 – [P0 MVP] Run unit and integration suites
- **Goal:** All P0 logic passes in one command.
- **Implements:** TST-001–010.
- **Owner / Time:** QA/All; 60 minutes.
- **Prerequisites:** Phases 2–12.
- **Why this step:** A repeatable suite prevents demo-only code.
- **Do this (micro-steps):**
  1. Run unit tests.
  2. Run integration tests.
  3. Run security tests.
- **Expected result:** Every test passes or known failures are explicitly linked.
- **Verify:** `pytest tests/unit tests/integration tests/security -q`.
- **If it fails:** Test data missing: run Phase 1 setup. Database unavailable: start Compose.
- **Git commit:** `git add tests && git commit -m "test: execute P0 unit integration and security suites"`
- **Done when:** P0 suite passes without skipped core tests.

## STEP 13.2 – [P0 MVP] Generate coverage
- **Goal:** P0 modules have measurable coverage.
- **Implements:** TST-001.
- **Owner / Time:** QA; 30 minutes.
- **Prerequisites:** Step 13.1.
- **Why this step:** Coverage identifies untested branches.
- **Do this (micro-steps):**
  1. Run pytest coverage.
  2. Generate HTML report.
- **Expected result:** Overall coverage >=80% and P0 modules >=90%.
- **Verify:** `pytest --cov=apps --cov-report=term-missing tests/unit`.
- **If it fails:** Low coverage: add edge-case tests, not fake assertions.
- **Git commit:** `git add coverage-report && git commit -m "test: publish coverage report"`
- **Done when:** Coverage report is reviewed.

## STEP 13.3 – [P0 MVP] Bench FPS and latency
- **Goal:** A raw benchmark report replaces external FALCON performance claims.
- **Implements:** NFR-001–003.
- **Owner / Time:** CV/ML; 90 minutes.
- **Prerequisites:** Reference hardware and 300-frame clip.
- **Why this step:** Judges need measured data for the team, not a copied paper result.
- **Do this (micro-steps):**
  1. Record hardware, OS, driver, model and frame size.
  2. Warm 5 minutes.
  3. Run 30-minute soak.
  4. Report P50/P95/P99 and FPS.
- **Expected result:** JSON and Markdown table exist.
- **Verify:** `python scripts/benchmark.py --duration 1800 --streams 1 --framesize 1080p`.
- **If it fails:** No GPU: benchmark CPU explicitly. FPS collapses: lower stream count and report target status.
- **Git commit:** `git add models/benchmarks && git commit -m "perf: publish own measured benchmark"`
- **Done when:** Report includes environment and raw logs.

## STEP 13.4 – [P1] Evaluate detector/tracker/OCR/FRS
- **Goal:** Model metrics are reported against held-out data.
- **Implements:** TST-005.
- **Owner / Time:** CV/ML; 180 minutes.
- **Prerequisites:** Licensed datasets.
- **Why this step:** PRD targets cannot be called passes without team measurements.
- **Do this (micro-steps):**
  1. Report mAP@0.5, mAP@0.5:0.95, precision and recall.
  2. Report MOTA, IDF1 and ID switches.
  3. Report exact-match and character accuracy.
  4. Report FAR/FRR if FRS is enabled.
- **Expected result:** A model report marks each target pass/fail/target-not-measured.
- **Verify:** `python scripts/evaluate_model.py --task all --dataset datasets/golden`.
- **If it fails:** Dataset leak: resplit site/time independent. License absent: remove the metric.
- **Git commit:** `git add models/benchmarks scripts/evaluate_model.py && git commit -m "perf: publish model evaluation report"`
- **Done when:** Every reported number includes dataset and hardware.

## STEP 13.5 – [P0 MVP] Run chaos and soak tests
- **Goal:** Camera loss, network loss and process kill recover safely.
- **Implements:** NFR-004–NFR-014.
- **Owner / Time:** DevOps/QA; 120 minutes.
- **Prerequisites:** Docker edge stack.
- **Why this step:** Lab-only happy paths are insufficient for border operations.
- **Do this (micro-steps):**
  1. Disconnect RTSP source.
  2. Disconnect HQ network.
  3. Kill API/container/process.
  4. Fill disk above alert threshold.
- **Expected result:** Each incident logs a status and recovers or degrades safely.
- **Verify:** `pytest tests/system tests/performance -q`.
- **If it fails:** Process no restart: systemd/Docker restart policy. Queue lost: persist SQLite/PostgreSQL queue.
- **Git commit:** `git add tests/system tests/performance && git commit -m "test: add chaos offline and soak coverage"`
- **Done when:** Recovery and controlled-degradation tests pass.

## Phase checklist
- [ ] Unit/integration/security suites pass.
- [ ] Coverage report exists.
- [ ] Own benchmark is measured.
- [ ] Model metrics are disclosed.
- [ ] Chaos tests pass.

## Phase demo
Show benchmark hardware table, FPS/latency, false alerts and chaos recovery.

## Rollback
Keep previous known benchmark; do not present a failed run as a target.

## Time summary
Phase 13 takes approximately 480 minutes.
