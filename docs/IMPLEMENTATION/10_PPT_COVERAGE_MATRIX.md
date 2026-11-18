# PPT-to-Product Coverage Matrix — Zero-Gap Plan Audit

**Audit date:** 2026-11-19 · **Source:** user-supplied PPT Fact Registry in the implementation-plan prompt.  
**Important:** this repository contains plans/specifications and a schema foundation, not a complete working product. `DOCUMENTED` means a concrete task/evidence path is recorded here; it does **not** mean implemented. All task-board rows currently have `Status=TODO`. Only use `IMPLEMENTED` or `MEASURED` after checked-in evidence proves it.

Status definitions: **IMPLEMENTED** = shipped behavior with passing evidence; **MEASURED** = observed result with reproducible method; **DOCUMENTED** = planned or sourced and explicitly not claimed as done; **STRETCH** = optional/later capability with entry criteria; **OUT-OF-SCOPE** = not promised/controlled outcome, with reason.

## PPT facts 01–47

| Item | Status | Plan task(s) / test or evidence | Location / caveat |
|---|---|---|---|
| PPT-01 Team FALCON, PS 26187, theme/category, blank Team ID | DOCUMENTED | F0-01, F15-05 / T15-05 | This file; [08_DEMO_AND_SUBMISSION_PLAN.md](./08_DEMO_AND_SUBMISSION_PLAN.md). Team ID remains fillable, must be filled at submission. |
| PPT-02 Existing CCTV at BOPs/check posts/border roads | DOCUMENTED | F0-05, F2-02, F14-01 / T2-02, T14-01 | Project context; real sites/cameras require authorization and inventory. |
| PPT-03 Conventional CCTV requires observation | DOCUMENTED | F15-04 / T15-04 | PPT-attributed problem statement; source study still needs verification. |
| PPT-04 Proprietary smart-camera dependence | DOCUMENTED | F10-04, F15-04 / T10-04, T15-04 | Comparative claim needs source/market verification. |
| PPT-05 Cost/scale/low-connectivity hardware challenge | DOCUMENTED | F11-01..04, F12-02, F14-01 / T11-01..04 | Cost/scope remain site-dependent; no numeric savings asserted. |
| PPT-06 Alert fatigue/delayed response/lost intelligence | DOCUMENTED | F4-05, F13-02, F14-02 / T4-05, T13-02, T14-02 | Potential problem context; improvement requires baseline and operator study. |
| PPT-07 20–35 min vigilance, ~50% detection, high false alarms | DOCUMENTED | F15-04, F13-02 / T15-04, T13-02 | Third-party/PPT claim pending exact study verification; never a Falcon measurement. |
| PPT-08 Software layer over ordinary CCTV | DOCUMENTED | F2-01..04, F3-01..03 / T2-01..04, T3-01..03 | Product goal; “any” camera must be qualified by compatibility tests. |
| PPT-09 RTSP/ONVIF smart-detector conversion | DOCUMENTED | F2-01..04 / T2-01..04 | Named devices/profiles required for compatibility claim. |
| PPT-10 Eight capabilities from shared pipeline | DOCUMENTED | F3-01..04, F4-01..09, F5-01..04, F6-01..04, F7-01..04, F8-01..03, F9-01..06 | Phased and feature-gated; not all eight are implemented or P0. |
| PPT-11 97% accuracy at 30 FPS benchmark | DOCUMENTED | F3-04, F13-02/03 / T3-04, T13-02/03 | Published target/reference from PPT; measure Falcon separately, no guarantee. |
| PPT-12 Fully offline core | DOCUMENTED | F11-01..04, F13-04 / T11-01..04, T13-04 | Must demonstrate local services without Internet; package/model acquisition may be staged. |
| PPT-13 Modular drone detection head | STRETCH | F3-04, F13-05 / T3-04, T13-05 | Head interface planned; drone model/data/evaluation are not MUST scope. |
| PPT-14 Four feature tiles: fence, suspicious activity, night, alerts/evidence | DOCUMENTED | F4-01..09, F6-01..04, F8-01..03, F9-03..06 / T4-01..09, T6-01..04, T8-01..03 | Night/behavior levels are staged; no invented model output. |
| PPT-15 Existing IP/ONVIF camera reuse | DOCUMENTED | F2-01..04, F10-03 / T2-01..04, T10-03 | Tested compatibility matrix only; no universal compatibility statement. |
| PPT-16 YOLO edge-inference pipeline called field-proven | DOCUMENTED | F3-01/04, F13-02/03 / T3-01/04, T13-02/03 | YOLO/edge integration planned; “field-proven” is not verified for Falcon. |
| PPT-17 Air-gapped/low-connectivity operation | DOCUMENTED | F11-01..04, F13-04 / T11-01..04, T13-04 | Test evidence required; not yet implemented. |
| PPT-18 Unified human/vehicle/face/ANPR/fence/behavior pipeline | DOCUMENTED | F3-01..04, F4-04, F5-01..04, F6-01..04, F7-01..04 / T3-01..04, T4-04 | Shared contracts planned; P1 modules remain separately gated. |
| PPT-19 Add models/heads without re-architecture | STRETCH | F3-04, F13-05 / T3-04, T13-05 | Verify extensibility with a new non-production head; UAV itself remains stretch. |
| PPT-20 REST/webhook C2/SOC integration | DOCUMENTED | F4-07, F10-01/02 / T4-07, T10-01/02 | Mock receiver first; real C2 requires partner contract/authorization. |
| PPT-21 Ingestion → five analytic branches → merge → alerts | DOCUMENTED | F0-04, F2-01..04, F3-01..04, F4-04..09 / T2-01..04, T3-01..04, T4-04..09 | Architecture path in 01/02 plan; branches phased by priority. |
| PPT-22 GStreamer/OpenCV, ONVIF driver, phone-stream swap and LUT pattern | DOCUMENTED | F0-05, F2-01..04 / T0-05, T2-01..04 | Prototype URL returned 404; LUT code not found. Implement interchangeable file/RTSP drivers; reuse claim prohibited until source is supplied. |
| PPT-23 YOLO person/vehicle, classifier, ByteTrack/DeepSORT, re-ID | DOCUMENTED | F3-01..04 / T3-01..04 | Optional type classifier not in MUST; cross-camera re-ID is P2/STRETCH (FR-016). |
| PPT-24 Roboflow fences, any-depth intrusion, timestamp/snapshot/REST/webhook | DOCUMENTED | F4-01..09 / T4-01..09 | Bottom-centre point, normalized versioned geometry; use authorized Roboflow export only. |
| PPT-25 Face print/landmarks, RetinaFace/YOLO-face, ArcFace/InsightFace, FAISS | DOCUMENTED | F7-01..04, F12-02/03 / T7-01..04 | PRD uses five-landmark 112×112 alignment and 512-D embedding; PPT’s “~80 landmarks” is not the API/model contract. FRS requires approval and remains off by default. |
| PPT-26 ANPR pipeline and <100 ms target | DOCUMENTED | F5-01..04, F13-03 / T5-01..04, T13-03 | 3–5-frame fusion/state validation; <100ms is a target until measured. |
| PPT-27 IR/thermal requires suitable sensor and tuned model | DOCUMENTED | F8-01..03 / T8-01..03 | Requires compatible sensor and labeled footage; not claimed from visible-light cameras. |
| PPT-28 Explainable heuristics; crawling/climbing later | DOCUMENTED | F6-01..04 / T6-01..04 | Heuristics planned; action recognition is stub-only/later (FR-056 P2). |
| PPT-29 Capture/preprocess/infer/track/rules/anomaly/alert/evidence workflow | DOCUMENTED | F2-01..04, F3-01..03, F4-01..09, F9-03..05 / T2-01..04, T3-01..03, T4-01..09 | Offline vertical slice; PRD/TRD defaults override prompt conflicts. |
| PPT-30 One-line pipeline flow | DOCUMENTED | F0-04, F15-02 / T0-04, T15-02 | Include exact one-line flow in architecture/README once generated; service order remains target architecture. |
| PPT-31 Exact stack/deployment/brand logos | DOCUMENTED | F0-01..03, F2-01..04, F3-04, F10-01, F11-04 / T0-01..03, T11-04 | TRD versions win; every library/license/runtime must be pinned and reviewed. Logo use is not evidence of integration. |
| PPT-32 Technical keyword list | DOCUMENTED | F15-03 / T15-03 plus per-keyword tasks | Every keyword is repeated in the dedicated keyword table; per-keyword status is listed below. |
| PPT-33 Feasibility and published benchmark claims | DOCUMENTED | F2-02, F3-04, F13-02/03 / T2-02, T13-02/03 | “Published/open-source/near-zero risk” and 97%@30FPS require source/compatibility evidence; no Falcon result inferred. |
| PPT-34 Operational feasibility, offline sync, pilot | DOCUMENTED | F11-01..04, F14-01..04 / T11-01..04, T14-01..04 | Pilot/rollout is conditional; operator and recovery measures required. |
| PPT-35 Reuse, open-source, 70–95% bandwidth, linear cost | DOCUMENTED | F10-04, F11-02, F12-05, F13-03, F14-03, F15-04 / T10-04, T13-03 | Cost and reduction are targets/assumptions until matched measurement and quotes. |
| PPT-36 Low bandwidth, phased modular rollout | DOCUMENTED | F11-01/02, F14-01, F14-03 / T11-01/02, T14-01/03 | Low-bandwidth bytes measured against baseline; FRS/behavior later only after gate. |
| PPT-37 Market sizes/CAGRs | DOCUMENTED | F15-04, F15-03 / T15-04, T15-03 | PPT-sourced to MRFR, unverified; exact edition/definition/date required before use. |
| PPT-38 Existing CCTV vs proprietary hardware USP | DOCUMENTED | F2-02, F10-03/04, F15-04 / T2-02, T10-03/04 | Positioning claim; compare scope and camera compatibility using primary sources. |
| PPT-39 Feasibility/viability keyword list | DOCUMENTED | F15-03 / T15-03 plus per-keyword tasks | Every keyword is repeated in the dedicated keyword table; per-keyword status is listed below. |
| PPT-40 24/7 monitoring, multi-analytic, edge, faster response benefits | DOCUMENTED | F11-01..04, F13-02/03, F14-01/02 / T11-01..04, T13-02/03 | Benefits are objectives; uptime and response improvements require measurements. |
| PPT-41 Situational awareness, personnel, evidence, integration impact | DOCUMENTED | F4-08/09, F10-01/02, F14-02 / T4-08/09, T14-02 | Potential impacts; pilot/user study evidence required. |
| PPT-42 Impact bubbles | DOCUMENTED | F13-02/03, F14-01/02, F15-03 / T13-02/03, T14-01/02 | Impact claim qualification and measurement plan; nationwide/reliability claims not asserted. |
| PPT-43 Weather/lighting and false-alarm challenges/solutions | DOCUMENTED | F3-01/03, F6-04, F8-03, F13-02/04/05 / T3-01/03, T13-02/04/05 | Multi-frame confirmation and class filtering tested; weather hardening is iterative, not solved by this plan. |
| PPT-44 Benefits/outcomes keyword list | DOCUMENTED | F15-03 / T15-03 plus per-keyword tasks | Every keyword is repeated in the dedicated keyword table; per-keyword status is listed below. |
| PPT-45 Research and references | DOCUMENTED | F0-05, F15-04 / T0-05, T15-04 | References and access results in 14; inaccessible/unknown source details are marked. |
| PPT-46 CIBMS/BOSS vs JARVIS vs FALCON table | DOCUMENTED | F10-03/04, F13-02/03, F15-04 / T10-03/04, T13-02/03 | Claims about retrofitting, JARVIS 99.7% LFW and capability gaps remain unverified pending primary sources. |
| PPT-47 Vercel prototype link | DOCUMENTED | F0-05, F15-04 / T0-05, T15-04 | Fetch returned HTTP 404 on 2026-11-19; ask team for working link/export before reuse; no behavior inferred. |

## PPT-32 keywords — technical/product

`DOCUMENTED` means mapped in the plan; STRETCH/OUT-OF-SCOPE rows explicitly limit the claim. All evidence is pending unless otherwise stated.

| Keyword | Status | Tasks / test | Evidence location / qualification |
|---|---|---|---|
| AI video analytics | DOCUMENTED | F3-01..04, F15-03 / T3-01..04 | Pipeline plan; implementation pending |
| Computer vision | DOCUMENTED | F2-04, F3-01..03 / T2-04, T3-01..03 | Preprocess/detection task plan |
| Deep learning | DOCUMENTED | F3-01, F5-01, F7-02, F8-02 / T3-01, T5-01, T7-02, T8-02 | Model license/performance not asserted |
| CNN | DOCUMENTED | F3-01, F5-01 / T3-01, T5-01 | Model architecture to be pinned and documented |
| YOLO | DOCUMENTED | F3-01/04 / T3-01/04 | Approved model/version required |
| Real-time object detection | DOCUMENTED | F3-01, F13-02/03 / T3-01, T13-02/03 | Latency/throughput measured; not claimed |
| Multi-object tracking | DOCUMENTED | F3-02/03 / T3-02/03 | Track identity and expiry tests |
| Object re-identification | STRETCH | F3-02, F13-05 / T3-02, T13-05 | PRD FR-016 P2; cross-camera matching needs validation and human confirmation |
| Anomaly detection | DOCUMENTED | F4-04, F6-01..04 / T4-04, T6-01..04 | Explainable rule anomalies only; no generic learned anomaly claim |
| Intrusion detection | DOCUMENTED | F4-01..05 / T4-01..05 | Fence crossing vertical slice |
| Motion detection | OUT-OF-SCOPE | F3-01, F6-04 / T3-01, T6-04 | Raw motion alone must not trigger security alerts; optional motion cues are not a detection substitute |
| Behavioural analysis | DOCUMENTED | F6-01..04 / T6-01..04 | Heuristics first; no claim that all behaviors are recognized |
| Crowd analytics | STRETCH | F6-02, F13-02 / T6-02, T13-02 | Group heuristic only; population-scale crowd analytics not validated |
| Perimeter security | DOCUMENTED | F4-01..09 / T4-01..09 | Software zone monitoring, not complete perimeter security solution |
| Automated alert generation | DOCUMENTED | F4-04..09 / T4-04..09 | Alert requires human review for response |
| Edge AI/computing | DOCUMENTED | F3-04, F11-03/04 / T3-04, T11-03/04 | Hardware-specific tests pending |
| Low-latency processing | DOCUMENTED | F13-02/03 / T13-02/03 | Measure p50/p95 before claim |
| Model inference optimisation | DOCUMENTED | F3-04, F13-02/03 / T3-04, T13-02/03 | ONNX/TensorRT targets; measured result pending |
| ONNX | DOCUMENTED | F3-04, F10-04 / T3-04, T10-04 | Export/import artifact and parity tests |
| TensorRT | DOCUMENTED | F3-04, F13-02 / T3-04, T13-02 | GPU/hardware availability required; otherwise untested |
| Border surveillance | DOCUMENTED | F14-01, F14-04 / T14-01/04 | Domain context; no field deployment claimed |
| CCTV infrastructure integration | DOCUMENTED | F2-01..04, F10-03 / T2-01..04, T10-03 | Specific tested profiles only |
| Perimeter monitoring | DOCUMENTED | F4-01..04 / T4-01..04 | Geometry/rule tests |
| Unauthorized intrusion detection | DOCUMENTED | F4-04/05, F14-02 / T4-04/05, T14-02 | Alert is a candidate for operator verification |
| Restricted-zone monitoring | DOCUMENTED | F4-01..04 / T4-01..04 | Zone schedule/version tests |
| Threat detection | DOCUMENTED | F4-04/05, F6-01..04 / T4-04/05, T6-01..04 | Rule-based events; not a guarantee of threat identification |
| Suspicious-activity recognition | DOCUMENTED | F6-01..04 / T6-01..04 | Explainable heuristics only |
| Thermal imaging integration | DOCUMENTED | F8-02/03 / T8-02/03 | Requires thermal sensor/data; otherwise untested |
| Night-vision analytics | DOCUMENTED | F8-01..03 / T8-01..03 | IR/night data required; not implied by visible camera |
| Multi-camera coordination | DOCUMENTED | F2-02, F10-03 / T2-02, T10-03 | PRD FR-008 P1; cross-camera re-ID remains separate P2 |
| Video Management System (VMS) integration | STRETCH | F10-03 / T10-03 | Adapter boundary/mock only until named VMS and supported API are tested |
| Sensor fusion | STRETCH | F10-03, F13-04 / T10-03, T13-04 | No sensor set/data/validated fusion model in workspace |
| Scalable architecture | DOCUMENTED | F0-04, F11-04, F13-03 / T0-04, T13-03 | Capacity tested per named hardware; nationwide scale not proven |
| Interoperable system | DOCUMENTED | F10-01..04 / T10-01..04 | OpenAPI/ONVIF/GeoJSON/MQTT adapters; conformance remains test-specific |
| Legacy CCTV integration | DOCUMENTED | F2-01..04 / T2-01..04 | Compatible device matrix required |
| Cloud-edge hybrid deployment | DOCUMENTED | F11-01/02 / T11-01/02 | Optional central sync; local core operation prioritized |
| API-based integration | DOCUMENTED | F10-01/02 / T10-01/02 | Versioned REST/webhook contract and mock |
| Low-bandwidth optimisation | DOCUMENTED | F11-02, F13-03 / T11-02, T13-03 | Measured vs matched baseline; 70–95% not assumed |
| Modular pipeline architecture | DOCUMENTED | F0-04, F3-04, F6-04 / T0-04, T3-04 | Plugin/model contract test |
| Real-time dashboard | DOCUMENTED | F9-01..06 / T9-01..06 | UI latency must be measured |
| Alert escalation workflow | DOCUMENTED | F4-05, F9-04 / T4-05, T9-04 | PRD severity/timers and transitions |
| Geo-tagged alerts | DOCUMENTED | F4-09, F9-06 / T4-09, T9-06 | Coordinates optional; map data/tiles must be valid |
| GIS integration | DOCUMENTED | F4-09, F9-06 / T4-09, T9-06 | Offline map data availability required |
| Transfer learning | DOCUMENTED | F0-06, F13-05 / T0-06, T13-05 | Dataset/license approval and measured held-out evaluation |
| Model fine-tuning | DOCUMENTED | F0-06, F13-05 / T0-06, T13-05 | Offline training workflow; promotion gated |
| False-positive reduction | DOCUMENTED | F3-01/03, F4-05, F6-04, F13-02 / T3-01/03, T4-05, T13-02 | Measure FP/camera-hour; no reduction percentage presumed |
| Explainable AI (XAI) | DOCUMENTED | F4-04, F6-01..04 / T4-04, T6-01..04 | Human-readable rule, threshold, track and rule version |
| On-device inference | DOCUMENTED | F3-04, F11-03 / T3-04, T11-03 | Tested runtime/hardware required |
| Temporal video analysis | DOCUMENTED | F3-03, F5-03, F6-01..03 / T3-03, T5-03, T6-01..03 | Track/fusion windows tested |
| Optical-flow analysis | STRETCH | F6-04, F13-05 / T6-04, T13-05 | Optional cue; not required for first slice |
| National security | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Societal outcome cannot be proven by this PoC |
| Force multiplier | OUT-OF-SCOPE | F14-02, F15-03 / T14-02, T15-03 | Potential impact, not a measured productivity result |
| Response-time reduction | DOCUMENTED | F13-03, F14-02 / T13-03, T14-02 | Measure baseline vs assisted workflow before claiming |
| Manpower optimisation | OUT-OF-SCOPE | F14-01/02 / T14-01/02 | Staffing policy outcome outside software acceptance scope |
| Proactive threat prevention | OUT-OF-SCOPE | F4-05, F14-04 / T4-05, T14-04 | Alerting is not proof of prevention |
| Cost-effective deployment | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Requires quotes/TCO, see 12_COST_AND_BENEFIT_MODEL.md |
| Existing-infrastructure utilisation | DOCUMENTED | F2-02, F10-03 / T2-02, T10-03 | Measured only for tested camera matrix |
| Scalable pan-India deployment | OUT-OF-SCOPE | F13-03, F14-01 / T13-03, T14-01 | No nationwide load, procurement or field evidence |
| 24×7 real-time monitoring | DOCUMENTED | F11-03/04, F13-04 / T11-03/04, T13-04 | Short tests do not establish 24×7 availability |
| Actionable intelligence | DOCUMENTED | F4-04/09, F14-02 / T4-04/09, T14-02 | Operator usability and context quality must be evaluated |
| Data-privacy compliance | DOCUMENTED | F7-01, F12-01..04, F14-04 / T7-01, T12-01..04, T14-04 | Checklist only; legal approval required |
| Secure data handling | DOCUMENTED | F12-01..05 / T12-01..05 | Threat tests and review required |
| Encrypted video storage | DOCUMENTED | F12-02 / T12-02 | Encryption-at-rest test pending |
| Role-based access control | DOCUMENTED | F1-04, F12-03 / T1-04, T12-03 | Negative site/role tests |
| Audit trail | DOCUMENTED | F1-04, F12-03/04 / T1-04, T12-03/04 | Append-only/hash-chain tests |
| Chain of custody | DOCUMENTED | F4-08, F12-04 / T4-08, T12-04 | Manifest, access records, signatures and verification |

## PPT-39 keywords — feasibility and viability

| Keyword | Status | Tasks / test | Evidence location / qualification |
|---|---|---|---|
| AI/ML feasibility | DOCUMENTED | F0-06, F3-04, F13-02 / T0-06, T13-02 | Dataset/hardware/model feasibility gate |
| Proof of Concept | DOCUMENTED | F4-01..09, F9-01..05, F15-01 / T4-01..09, T15-01 | Lab PoC only; not field validation |
| Technology Readiness Level (TRL) | DOCUMENTED | F14-01, F15-03 / T14-01, T15-03 | Baseline unassessed; provisional lab PoC target requires reviewer assessment |
| Legacy-CCTV interoperability | DOCUMENTED | F2-01..04, F10-03 / T2-01..04, T10-03 | Explicit device/profile matrix |
| Hardware-software compatibility | DOCUMENTED | F0-02, F3-04, F11-04 / T0-02, T3-04, T11-04 | Test exact versions/hardware; Jetson untested absent device |
| Bandwidth-constraint analysis | DOCUMENTED | F11-02, F13-03 / T11-02, T13-03 | Measure bytes against matched baseline |
| Real-time processing feasibility | DOCUMENTED | F3-04, F13-02/03 / T3-04, T13-02/03 | Report measured FPS and latency; targets are not results |
| Edge-deployment feasibility | DOCUMENTED | F11-03/04, F13-04 / T11-03/04, T13-04 | Device-specific deployment tests |
| Scalability assessment | DOCUMENTED | F13-03, F14-01 / T13-03, T14-01 | Measure per-node/site; 16-node/pan-India remains unproven |
| Pilot deployment | DOCUMENTED | F14-01..04 / T14-01..04 | Conditional on approval; no live pilot assumed |
| Phased rollout strategy | DOCUMENTED | F14-01 / T14-01 | Stage gates in 11_PILOT_AND_ROLLOUT_PLAN.md |
| Low-cost implementation | DOCUMENTED | F12-05, F14-03, F15-04 / T14-03, T15-04 | Needs quote-based cost model |
| Minimal infrastructure overhaul | DOCUMENTED | F2-02, F10-03, F14-03 / T2-02, T10-03 | Validate by site survey; not universal |
| Open-source model utilisation | DOCUMENTED | F0-06, F3-04, F12-05 / T0-06, T3-04, T12-05 | Verify each model's license; “open source” not assumed for every weight |
| Pretrained-model adaptation | DOCUMENTED | F0-06, F13-05 / T0-06, T13-05 | Transfer/fine-tuning requires licensed data and held-out test |
| Dataset availability | DOCUMENTED | F0-06 / T0-06 | Inventory/license and access gate |
| Data-annotation requirement | DOCUMENTED | F0-06, F13-02 / T0-06, T13-02 | Annotation guide and reviewer protocol |
| Computational-resource requirement | DOCUMENTED | F3-04, F13-03 / T3-04, T13-03 | Record CPU/GPU/RAM/thermal |
| GPU/Edge-TPU requirement | DOCUMENTED | F0-02, F3-04, F11-03 / T3-04, T11-03 | Optional target hardware; CPU fallback path |
| Network-latency constraint | DOCUMENTED | F2-03, F13-03 / T2-03, T13-03 | Measure local/central paths separately |
| Environmental robustness (fog, low light, adverse weather) | DOCUMENTED | F8-03, F13-04 / T8-03, T13-04 | Condition-stratified test; phased hardening |
| False-positive/negative risk | DOCUMENTED | F3-01/03, F13-02 / T3-01/03, T13-02 | FP/hour, FN/event measured |
| Risk-mitigation strategy | DOCUMENTED | F0-01..F15-05 / T15-03 | 07_RISK_REGISTER.md |
| Technical risk | DOCUMENTED | F0-02, F1-01, F2-02, F3-04 / T1-01, T2-02, T3-04 | Register includes toolchain/DB/camera/model risks |
| Operational risk | DOCUMENTED | F11-03/04, F14-01..04 / T11-03/04, T14-01..04 | Runbooks, human review and rollback |
| Regulatory-compliance risk | DOCUMENTED | F12-01, F14-04 / T12-01, T14-04 | Review checklist; no legal compliance claim |
| Data-privacy risk | DOCUMENTED | F7-01, F12-01..04 / T7-01, T12-01..04 | FRS gated, minimize, encrypt, retain/audit |
| Cybersecurity risk | DOCUMENTED | F12-01..05 / T12-01..05 | STRIDE and security gates |
| Integration risk | DOCUMENTED | F10-01..03 / T10-01..03 | Contract-first and mock receiver |
| Adoption risk | DOCUMENTED | F14-02/04 / T14-02/04 | Operator feedback/training |
| Change management | DOCUMENTED | F14-02/04 / T14-02/04 | Stakeholder review and transition |
| Stakeholder training requirement | DOCUMENTED | F14-02 / T14-02 | Scenario-based SOP/training |
| Maintenance and support feasibility | DOCUMENTED | F14-03 / T14-03 | Support roles, update/restore evidence |
| Cost-benefit analysis | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Editable assumptions and formulas; input quotes required |
| CapEx | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Formula only until quotes |
| OpEx | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Formula only until energy/support/network inputs |
| ROI | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | No ROI assertion without comparable baseline |
| TCO | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Horizon and source inputs must be stated |
| Budget feasibility | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Team/finance to populate model |
| Funding model | DOCUMENTED | F14-01, F14-04 / T14-01, T14-04 | No funding source identified; decision remains outside PoC |
| Public-Private Partnership (PPP) potential | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Requires government/procurement/legal sponsor; no PPP claim |
| Government procurement alignment | DOCUMENTED | F14-04 / T14-04 | Checklist only; current guidance must be reviewed by authority |
| Policy alignment | DOCUMENTED | F14-04 / T14-04 | Review requirement; no policy approval asserted |
| Ministry-guidelines compliance | DOCUMENTED | F14-04 / T14-04 | Verify current applicable guidelines with qualified reviewer |
| Long-term/environmental sustainability | DOCUMENTED | F14-03 / T14-03 | Measure replacement, e-waste and lifecycle; no claim yet |
| Energy efficiency | DOCUMENTED | F14-03, F13-03 / T14-03, T13-03 | Measure watts/camera-hour on named device |
| Maintenance-cost reduction | OUT-OF-SCOPE | F14-03, F15-04 / T14-03, T15-04 | Cannot assert until comparable historical cost evidence exists |
| Vendor lock-in mitigation | DOCUMENTED | F10-04, F12-05 / T10-04, T12-05 | Round-trip open-format export test |
| Cross-platform compatibility | DOCUMENTED | F0-02, F3-04, F10-04 / T0-02, T3-04, T10-04 | Platform matrix required; not universal |
| Standardisation compliance | DOCUMENTED | F10-01/03, F14-04 / T10-01/03, T14-04 | Standards review and conformance tests required |
| Interoperability with VMS | STRETCH | F10-03 / T10-03 | Named VMS protocol/certification not provided |
| Interoperability with C4I | STRETCH | F10-01..03 / T10-01..03 | Mock only until approved C4I partner contract/test rig exists |
| Market viability | DOCUMENTED | F15-04 / T15-04 | Market figures and competitor sources unverified |
| Deployment timeline | DOCUMENTED | F0-01..F15-05 / T15-03 | Eight weeks is editable planning baseline, no finale date found |
| Resource availability | DOCUMENTED | F0-02, F0-06, F14-01 / T0-02, T0-06, T14-01 | Confirm roster, hardware and data at kickoff |
| Technical-expertise and manpower requirement | DOCUMENTED | F0-01, F14-02 / T0-01, T14-02 | 6-person allocation is assumption, not confirmed roster |
| Contingency planning | DOCUMENTED | F11-03, F15-05 / T11-03, T15-05 | Fallback/demo backup procedure |
| Fallback mechanism | DOCUMENTED | F11-03, F15-01/05 / T11-03, T15-01/05 | CPU/mock/recorded fallback clearly labeled |
| Redundancy planning | DOCUMENTED | F11-03/04, F14-03 / T11-03/04, T14-03 | Test failure/recovery; no HA guarantee |
| System-uptime guarantee | OUT-OF-SCOPE | F13-04, F14-03 / T13-04, T14-03 | No production SLA or long-term measurement supports a guarantee |

## PPT-44 keywords — impacts and benefits

These are potential societal/operational outcomes. A product task is not proof that the outcome occurred. Where the outcome depends on staffing, policy, environment or adversary behavior, it is explicitly not guaranteed.

| Keyword | Status | Tasks / test | Evidence location / qualification |
|---|---|---|---|
| National-security enhancement | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Cannot establish national-security outcome from a PoC |
| Border-security strengthening | DOCUMENTED | F14-01/04 / T14-01/04 | Intended context; site-level pilot evidence required |
| Real-time situational awareness | DOCUMENTED | F9-03/04, F13-03 / T9-03/04, T13-03 | UI data freshness/latency measured |
| Force multiplier | OUT-OF-SCOPE | F14-02, F15-03 / T14-02, T15-03 | Potential impact, not measured staffing outcome |
| Manpower optimisation | OUT-OF-SCOPE | F14-02 / T14-02 | Staffing outcome beyond system scope |
| Reduced human error | DOCUMENTED | F13-02, F14-02 / T13-02, T14-02 | Requires comparative operator study |
| 24×7 monitoring | DOCUMENTED | F11-03/04, F13-04 / T11-03/04, T13-04 | Uptime period must be stated; no guarantee |
| Faster incident response | DOCUMENTED | F13-03, F14-02 / T13-03, T14-02 | Baseline and assisted response time needed |
| Early-warning system | DOCUMENTED | F4-04/05, F14-02 / T4-04/05, T14-02 | Rule alert only; no threat prevention guarantee |
| Actionable intelligence | DOCUMENTED | F4-09, F9-05, F14-02 / T4-09, T9-05, T14-02 | Operator usefulness requires study |
| Improved decision-making | OUT-OF-SCOPE | F14-02, F15-03 / T14-02, T15-03 | Outcome cannot be inferred without user study |
| Cost-effective security | DOCUMENTED | F14-03, F15-04 / T14-03, T15-04 | Quote-based comparison required |
| Reduced long-term cost | OUT-OF-SCOPE | F14-03, F15-04 / T14-03, T15-04 | Requires multi-year comparable cost evidence |
| Optimal use of existing infrastructure | DOCUMENTED | F2-02, F14-01 / T2-02, T14-01 | Device/site compatibility and capacity testing required |
| Pan-India deployment | OUT-OF-SCOPE | F13-03, F14-01 / T13-03, T14-01 | Not tested across nationwide conditions/procurement |
| Reduced manual surveillance burden | DOCUMENTED | F14-02 / T14-02 | Operator task study needed |
| Fatigue-free monitoring | OUT-OF-SCOPE | F14-02, F15-03 / T14-02, T15-03 | Automation does not eliminate fatigue or human oversight |
| Elimination of blind spots | OUT-OF-SCOPE | F14-01, F15-03 / T14-01, T15-03 | Cameras/occlusion create blind spots; cannot promise elimination |
| Reduced false-alarm rate | DOCUMENTED | F13-02 / T13-02 | Must compare FP/camera-hour against defined baseline |
| Evidence-based decision support | DOCUMENTED | F4-08/09, F12-04, F14-02 / T4-08/09, T12-04 | Evidence integrity and human review |
| Deterrence against infiltration | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Behavioral/adversary outcome not proven |
| Reduced illegal crossings | OUT-OF-SCOPE | F14-01, F15-03 / T14-01, T15-03 | Requires long-term operational evaluation |
| Inter-force coordination | DOCUMENTED | F10-01/02, F14-04 / T10-01/02, T14-04 | Partner agreement/integration not present |
| Improved C2 | DOCUMENTED | F10-01/02, F13-03 / T10-01/02, T13-03 | Mock receiver only until integration tested |
| Centralised monitoring | DOCUMENTED | F11-01, F10-01 / T11-01, T10-01 | Optional central sync; local core remains |
| Support for BSF | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | No agency endorsement or deployment approval |
| Socio-economic stability in border areas | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Societal outcome not attributable to this software plan |
| Public safety | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Requires deployment-level impact assessment |
| Community trust | DOCUMENTED | F12-01, F14-02/04 / T12-01, T14-02/04 | Requires consultation and governance, not a feature claim |
| Reduction in smuggling/trafficking | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Enforcement outcome beyond system evidence |
| Support for anti-terrorism operations | OUT-OF-SCOPE | F14-04, F15-03 / T14-04, T15-03 | Sensitive operational outcome; no claim or target here |
| Improved resource allocation | DOCUMENTED | F14-02, F15-03 / T14-02, T15-03 | Requires operator/resource utilization study |
| Data-backed policy making | DOCUMENTED | F4-09, F14-04 / T4-09, T14-04 | Aggregate data governance and quality review required |
| Atmanirbhar Bharat alignment | DOCUMENTED | F10-04, F12-05, F14-04 / T10-04, T12-05, T14-04 | Alignment statement needs review; no endorsement implied |
| Indigenous AI | DOCUMENTED | F0-06, F3-04, F14-04 / T0-06, T3-04, T14-04 | Model origin/license must be verified; no indigenous claim without provenance |
| Future-ready system | DOCUMENTED | F0-04, F3-04, F10-04 / T0-04, T3-04, T10-04 | Modularity is a design goal, not a guarantee of future compatibility |
| Replicable model for other sensitive zones | DOCUMENTED | F10-03, F14-01 / T10-03, T14-01 | Requires separate site/security/protocol validation |
| Inter-agency data sharing | STRETCH | F10-01..03, F14-04 / T10-01..03, T14-04 | Needs agreements, data governance and approved partner integration |
| Reduced operational downtime | DOCUMENTED | F11-03/04, F13-04 / T11-03/04, T13-04 | Measure recovery/downtime; no guarantee |
| Improved audit and accountability | DOCUMENTED | F12-03/04, F14-04 / T12-03/04, T14-04 | Audit-chain tests and governance review |
| Transparent security operations | DOCUMENTED | F12-01..04, F14-02/04 / T12-01..04, T14-02/04 | Explainable alerts, access logs, human review; operational transparency requires policy |

## Self-audit summary

- **COVERAGE: 214/214 items covered, 10 stretch, 24 out-of-scope, 0 missing.** Coverage means every PPT registry fact/keyword has an explicit planning status and trace; it does not mean the feature is built.
- Fact registry: PPT-01 through PPT-47 each has one row.
- PPT-32 technical keyword list: 66 terms, one row each.
- PPT-39 feasibility list: 60 terms, one row each, including separate compliance-risk and cost sub-items.
- PPT-44 impact list: 41 phrases, one row each, including separate Atmanirbhar Bharat and indigenous AI terms.
- All statuses are honest for a plan-only workspace; all tasks remain TODO. Run the final row/ID audit after task changes and before submission. No “implemented” or “measured” status is allowed without artifact evidence.
