# Pilot and Rollout Plan

## Readiness and TRL statement

- **Current verified readiness:** documentation/schema foundation only; no running service, field deployment, or measured model result exists in the reviewed workspace.
- **Current TRL:** not independently assessed. For planning only, a reviewer may classify the present concept/specification near TRL 2; this is not an official project claim. Team lead must request mentor/judge assessment and record the basis before submission.
- **Hackathon target:** reproducible laboratory proof-of-concept with a local video source and demonstrable end-to-end fence alert. A provisional TRL-3-style lab validation is a planning target, not a certification.
- **Not a target for this plan:** border-post operational deployment, production certification, 99.5% monthly availability guarantee, pan-India scale, or autonomous security decisions.

## Phased rollout gates

| Stage | Entry criteria | Activities | Exit criteria / decision |
|---|---|---|---|
| 0 — Desk review | Product/technical documents and owners confirmed | Resolve API/role/schema gaps; check camera, dataset, model, privacy and system licenses | Signed scope, hazard/privacy review, test plan, no unresolved P0 data contract |
| 1 — Lab PoC | M1/M2 passed; authorized footage/models; isolated network | Local file/camera source, shared detection, fence, alert, evidence, dashboard, integrity test | Reproducible tests; measured baseline; known limitations and rollback documented |
| 2 — Shadow pilot | Site authorization, privacy/legal approval, safe install, trained operators, rollback | Read-only parallel operation; operators compare alerts to current procedure; no automated enforcement | Pre-agreed accuracy/FP rate, uptime, recovery, operator acceptance and privacy criteria met |
| 3 — Controlled operational pilot | Shadow exit review and risk approval | Limited cameras/sites; on-call support, change control, retention, update and incident process | Independent review, evidence chain, support/SLA and failure recovery accepted |
| 4 — Cluster/sector scale | Pilot acceptance plus interoperability/security sign-off | Incremental site additions; resource sizing and cross-site monitoring; training refresh | Capacity and cost measured per site; no regression; accountable program owner approves |
| 5 — Wider rollout | Procurement, policy, compliance, budget, support and interoperability approvals | Replicable deployment packs and standard operating model | Formal deployment decision; this plan does not assert such approvals exist |

## Site selection criteria

Choose a controlled, authorized test location with a site owner, operator representatives, safe network isolation, camera/NVR model/codec documentation, stable power, storage, time synchronization, legal/privacy review, approved sample footage, recovery access, and a fallback to existing monitoring. Exclude live operational/border footage unless explicit authorization, handling rules, retention and incident contacts are recorded.

## Success KPI template

Set thresholds with stakeholders before collecting pilot data. These are measurements to gather, not promised values.

| KPI | Measurement | Evidence needed |
|---|---|---|
| Detection quality | Precision/recall per class and condition, with confidence intervals | Held-out labeled footage, split and reviewer protocol |
| False alarm burden | False alerts per camera-hour and operator-confirmation rate | Annotated camera-hours and action outcomes |
| Missed event rate | False negatives per scripted/observed crossing | Ground truth and sampling method |
| Alert latency | p50/p95 capture timestamp to alert visible/actionable | Monotonic timestamps, edge hardware and network |
| Service availability | Measured uptime excluding declared maintenance | Defined monitor, observation period and exclusions |
| Camera recovery | Reconnect success and time after link restored | Repeated disconnect test on named devices |
| Evidence integrity | Valid/tampered/failed verification pass rate | Test fixtures, signatures, manifests and audit |
| Offline durability | Events/evidence retained through 72h disconnect and restart | Queue volume, storage use, recovery and replay logs |
| Bandwidth | Bytes under matched edge and baseline profile | Matched video duration, quality and evidence policy |
| Operator usability | Task success/time for acknowledge/verify/escalate/retrieve | Observed users, consent, task protocol and sample count |
| Cost/energy | Edge hardware, storage, installation, power, support costs | Local quotes and power measurements, separated from assumptions |

## Training, SOP and support

- Operator training: camera health, alert severity, visual evidence, false-positive feedback, escalation, privacy, and not treating a model match as proof.
- Supervisor training: role/site access, watchlist governance, review approval, handover, escalation, legal hold and incident response.
- Administrator training: credentials, certificate/key rotation, patch/rollback, backup/restore, disk thresholds and access review.
- ML maintainer training: dataset provenance, annotation QA, model evaluation/signing, staged promotion, rollback and performance drift.
- Auditor training: evidence chain verification, purpose/access logs, export manifests and limitations of a hash chain.
- Support: define primary/secondary contact, triage severity, response window, escalation to camera/network/model owners, incident evidence retention and update cadence before pilot.

## Update and rollback

Stage signed software/model packages; verify SBOM, checksum/signature and DB migration compatibility; backup config/data; run offline tests; deploy canary; monitor health/false-alert metrics; rollback on criteria breach. Do not silently auto-promote a candidate model. Air-gapped deployment package and rollback image are required before field use.

## Policy, procurement and sustainability review (not legal claims)

For any government/defense rollout, qualified stakeholders must check current procurement and ministry guidelines, standards, data-handling rules, security authorization, site safety, retention and inter-agency agreements. This plan does not assert compliance, procurement eligibility, PPP approval, or agency endorsement.

Measure edge energy per camera-hour, cooling/power requirements, replacement cycle, battery/UPS needs, e-waste handling, travel/maintenance burden and storage refresh. Record each as measured, vendor-specified or assumed. Open standards and exportable model/data formats reduce lock-in but do not alone guarantee portability.

