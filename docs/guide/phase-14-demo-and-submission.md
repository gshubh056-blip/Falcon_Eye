# Phase 14 - Demo and Submission

## STEP 14.1 – [P0 MVP] Seed reproducible demo data
- **Goal:** The judges see a complete scenario without real identities or field hardware.
- **Implements:** Demo requirements.
- **Owner / Time:** Frontend/Backend; 60 minutes.
- **Prerequisites:** M2–M4 pass.
- **Why this step:** A reproducible seed avoids race conditions and privacy risk.
- **Do this (micro-steps):**
  1. Create synthetic camera, zone and alert records.
  2. Reset demo database in disposable Docker volume.
  3. Use synthetic plate and consented face test assets.
- **Expected result:** One demo reset creates known alert sequences.
- **Verify:** `python scripts/seed_demo.py --reset`.
- **If it fails:** Production database: block reset unless `FALCON_ENV=demo`.
- **Git commit:** `git add scripts/seed_demo.py && git commit -m "demo: add reproducible demo seed"`
- **Done when:** Reset/reseed produces the same demo route.

## STEP 14.2 – [P0 MVP] Prepare the live demo script
- **Goal:** The 10-minute SIH demo has one deterministic route.
- **Implements:** TST-010.
- **Owner / Time:** Team lead; 45 minutes.
- **Prerequisites:** Step 14.1.
- **Why this step:** Judge timing is more important than unexplained feature count.
- **Do this (micro-steps):**
  1. Open live stream.
  2. Draw crossing zone.
  3. Show detection/tracking.
  4. Show alert/evidence.
  5. Disconnect/restore sync.
  6. Tamper and verify evidence.
- **Expected result:** Script completes in 8–10 minutes.
- **Verify:** Rehearse three times and time each section.
- **If it fails:** Live stream drops: switch to preloaded MediaMTX recording.
- **Git commit:** `git commit --allow-empty -m "docs: rehearse ordered SIH demo"`
- **Done when:** Three rehearsal runs finish without manual database repair.

## STEP 14.3 – [P0 MVP] Prepare fallback media
- **Goal:** The demo remains usable if internet, cameras or GPU fail.
- **Implements:** Demo fallback.
- **Owner / Time:** DevOps/CV; 45 minutes.
- **Prerequisites:** Step 14.2.
- **Why this step:** A recorded backup prevents a hardware failure becoming a submission failure.
- **Do this (micro-steps):**
  1. Record full screen and terminal evidence.
  2. Export H264-compatible loop clip.
  3. Preload dashboard screenshot and benchmark PDF.
- **Expected result:** Single offline folder opens without internet.
- **Verify:** Disconnect network and run the fallback.
- **If it fails:** Codec missing: transcode MP4 H264/AAC.
- **Git commit:** `git add docs/demo && git commit -m "demo: add offline fallback assets"`
- **Done when:** Fallback demo runs for 10 minutes.

## STEP 14.4 – [P0 MVP] Update README and architecture diagram
- **Goal:** A new contributor can run the MVP in 10 minutes.
- **Implements:** PRD and TRD documentation.
- **Owner / Time:** Docs/DevOps; 75 minutes.
- **Prerequisites:** Final Compose commands.
- **Why this step:** Repository evidence demonstrates engineering quality.
- **Do this (micro-steps):**
  1. Add quick start, architecture Mermaid, test commands and demo credentials.
  2. Add badges only after real CI and license checks.
  3. Link PRD/TRD and guide.
- **Expected result:** A clean clone starts documented demo services.
- **Verify:** Follow README on a second laptop or user.
- **If it fails:** Missing env: correct `.env.example`. Port conflict: document stop commands.
- **Git commit:** `git add README.md docs && git commit -m "docs: finalize repository quick start"`
- **Done when:** A second student completes Quick Start.

## STEP 14.5 – [P0 MVP] Update PPT with measured results
- **Goal:** Slides replace external numbers with measured FALCON numbers.
- **Implements:** Claims-to-verify table.
- **Owner / Time:** Team lead/ML; 90 minutes.
- **Prerequisites:** Benchmarks from Phase 13.
- **Why this step:** Unsupported numbers weaken credibility.
- **Do this (micro-steps):**
  1. Label external claims with source or remove.
  2. Insert own hardware/FPS/latency/accuracy table.
  3. Label every unmeasured target.
  4. Update CIBMS/BOSS/JARVIS comparison only with verified source.
- **Expected result:** Slides distinguish external claim and measured team result.
- **Verify:** Peer checklist against `docs/TRD.md` and PRD claims table.
- **If it fails:** No measured value: label target – to be measured.
- **Git commit:** `git add presentation docs && git commit -m "docs: replace external claims with benchmark results"`
- **Done when:** Every metric has source or team methodology.

## Phase checklist
- [ ] Demo reset works.
- [ ] 10-minute script passes.
- [ ] Offline fallback passes.
- [ ] README quick start passes.
- [ ] PPT uses measured values.

## Phase demo
Run the final 10-minute judge flow once without repairing state.

## Rollback
Restore previous demo seed and recorded fallback; do not commit private data.

## Time summary
Phase 14 takes approximately 315 minutes.
