# Demo and Submission Plan

## Five-minute judge walkthrough

The demo is a local, offline-first PoC using a licensed video file as a camera source unless a named real IP camera has passed the compatibility test. Any seed/injected event is labeled **SYNTHETIC DEMO EVENT**. Never describe replay or injected JSON as model inference.

| Time | Show | Action and expected result | Evidence |
|---|---|---|---|
| 0:00–0:25 | Site/camera overview | Start `make demo`; show local health and a camera source. Explain existing IP cameras use the same driver interface; identify whether this run is file or RTSP. | Startup log/config with source type |
| 0:25–1:05 | Detection and tracking | Show person/vehicle boxes, confidence, frame timestamp and confirmed track. State the tested model/runtime and whether output is real inference or fixture. | Model hash, benchmark page, UI |
| 1:05–1:45 | Fence breach | Show versioned line/polygon and bottom-centre point; replay/inject a crossing. Rule explanation identifies direction, class, track and rule version. | Rule/event JSON and fence editor |
| 1:45–2:20 | Alert, escalation and siren hook | Show severity, alert lifecycle, dedupe and authorized acknowledgement. Siren is a mock unless connected relay is explicitly tested. | Alert detail, action audit, mock receiver |
| 2:20–3:00 | Evidence | Open annotated snapshot and 10-second pre/post clip; show manifest and SHA-256. | Evidence access log and metadata |
| 3:00–3:35 | Integrity verify | Verify intact evidence, then run a safe test-copy tamper to show rejection. Do not alter source evidence. | `/api/v1/evidence/{event_id}/verify` response |
| 3:35–4:10 | Offline | Disconnect HQ/Internet path in a controlled lab; local camera, alert, dashboard and outbox remain usable. | Local health + queued sync count |
| 4:10–4:35 | Resync | Restore link to local mock central receiver; show idempotent transfer and cursor progress. | Sync log; duplicate replay count remains zero |
| 4:35–5:00 | GIS and close | Show geo-tagged event/camera/fence only if coordinates/tiles are real test data. Summarize measured results, targets, limitations and next phase. | Benchmark/traceability summary |

### Setup and fail-safe

1. Use [09_DEV_ENVIRONMENT_RUNBOOK.md](./09_DEV_ENVIRONMENT_RUNBOOK.md) on the actual demo machine at least one day before presentation.
2. Pre-stage only approved/licensed video, model weights, map tiles, Python wheels, Node packages, container images, and DB seed; verify checksums.
3. Keep all external C2/webhooks pointed to a local mock receiver. Use dummy users and test secrets. Never connect to a real border camera or operational relay without authorization.
4. Rehearse a fully offline run. If model inference fails, switch to a labeled recorded run or labeled synthetic event; do not claim live detection.
5. Keep a backup recording, static screenshots with captions, printed architecture, test report and known limitations. State when backup playback begins.

## Judge Q&A sheet

| Question | Accurate answer structure |
|---|---|
| What accuracy does Falcon achieve? | Give only the measured dataset/hardware/model result from `docs/BENCHMARKS.md`. The 97% @30FPS item is a PPT-sourced published target/reference, not our measured result. If no qualifying measurement exists, say so. |
| Does it work offline? | Core capture, inference, local API/DB, alerts and evidence are designed to operate at the edge; demonstrate only functions exercised in the offline test. Sync is store-and-forward when a central link is configured. |
| How much does it cost? | Use editable assumptions in `12_COST_AND_BENEFIT_MODEL.md`; show local quotes, energy/storage and deployment count. Do not present market or ROI estimates as measured facts. |
| How does it scale? | Explain one edge node per site/cluster, bounded queues and measured capacity per named hardware. Nationwide scale is potential, not tested. |
| How is privacy handled? | Site-scoped RBAC, purpose-bound access, retention/legal hold, evidence encryption, audit, face feature gate and human review. Face recognition stays off without approved legal basis and policy. |
| Why not smart cameras? | Falcon's goal is to add software analytics to compatible installed CCTV and avoid a camera forklift upgrade. The exact supported camera matrix is bounded by tests. |
| How does it compare to CIBMS/BOSS? | Explain these are different system scopes and acknowledge that the PPT comparison needs source/spec verification. Do not claim “not retrofittable” unless a primary procurement/spec source supports it. |
| How does it compare to JARVIS by Staqu? | Do not repeat the PPT's 99.7% LFW or product-gap claims as verified without dated primary sources and matched conditions. Focus on the Falcon PoC's measured behavior and documented integration goals. |
| Why a hash chain / blockchain theme? | Demonstrate SHA-256 content hashes, previous-hash linkage, signature/Merkle verification and tamper detection. The local ledger is tamper-evident, not a public blockchain or proof of truth; an external anchor is optional stretch. |
| How are false alarms reduced? | Class-aware person/vehicle filtering, ROI/size/NMS thresholds, 3-frame track confirmation, explainable zone rules, cooldown/deduplication and measured FP per camera-hour. |
| What about weather? | Outdoor glare/rain/fog/night are known hardening tasks. Show only test conditions/results; degradation flags and human review do not guarantee detection. |
| Is there face recognition? | Only if the approval gate, license, privacy controls, threshold evaluation and review flow are complete. Otherwise show disabled state and explain why. |
| What is the response-time improvement? | Quote measured camera-to-alert latency and operator task results only; do not convert the PPT’s “minutes/hours to near-instant” into a Falcon claim without study. |
| What is your TRL? | Give the reviewer-assessed baseline/target recorded in `11_PILOT_AND_ROLLOUT_PLAN.md`. Until approved, describe as a lab PoC, not field-proven or production-ready. |

## Submission checklist

- [ ] Team name FALCON and banner “FALCONNN” are consistent.
- [ ] PS ID 26187, Software category, and Blockchain & Cybersecurity theme are correct.
- [ ] **Team ID:** ____________________ filled from official registration (owner: Team lead; due: before final upload).
- [ ] `10_PPT_COVERAGE_MATRIX.md` has every fact and keyword, a status, task, test/evidence, repo location, and reason for stretch/out-of-scope.
- [ ] All measured claims include dataset, hardware, software/model versions and method; PPT-sourced values are attributed or removed.
- [ ] Prototype review and prior-driver search findings are accurately stated; no implied reuse.
- [ ] Security/privacy, data/model licenses, face gate and safe-demo controls are reviewed.
- [ ] Clean-machine setup, offline mode, rollback and backup demo were rehearsed.
- [ ] API/architecture/ERD and known gaps reflect the actual built version, not aspirational files.
- [ ] Default demo credentials are temporary, local-only, and rotated/removed after demo.
- [ ] No secrets, sensitive camera URLs, face data, personal data or unlicensed footage are in source/history.
- [ ] Final package includes release commit/version, test reports, risk summary, operator guide and known limitations.

