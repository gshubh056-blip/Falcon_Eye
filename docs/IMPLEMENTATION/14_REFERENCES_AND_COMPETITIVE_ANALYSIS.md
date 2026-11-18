# References and Competitive Analysis

**Review date:** 2026-11-19. Links named in the PPT are references to verify, not endorsements or proof that Falcon achieves the same results. The prototype link returned 404 during this review. A failed fetch is not evidence that a source or claim is false; preserve the access status and obtain the exact citation before external claims.

## PPT-45 references: use and source status

| Reference | Link / status | What Falcon uses it for | Caveat / follow-up |
|---|---|---|---|
| Ultralytics security alarm system guide | [Ultralytics guide](https://docs.ultralytics.com/guides/security-alarm-system/) · fetched 2026-11-19 | Example of applying YOLO detection to a security-alert workflow and existing camera/video inputs. | Current page identifies YOLO26 and email alarm examples; it is not evidence for Falcon's edge performance, licensing decision, or security readiness. Review model/license/version before adoption. |
| ROS 2 + YOLOv11 real-time detection/tracking walkthrough | [FreeCodeCamp search for the named walkthrough](https://www.freecodecamp.org/news/search/?query=ROS%202%20YOLOv11%20real-time%20object%20detection%20tracking) · exact article not confirmed | Potential reference for ROS 2 integration and real-time detection/tracking patterns. | Exact article URL/title/author were not provided or verified; do not cite technical results until found and reviewed. ROS is not a mandated Falcon dependency. |
| JARVIS by Staqu | [Staqu site](https://staqu.com/) · primary product source needs locating | Product-category context for AI video analytics on existing CCTV. | The PPT’s 99.7% LFW and capability-gap claims are unverified here; do not repeat as established fact without a dated primary source and metric conditions. |
| “Video-based Real-Time Intrusion Detection using YOLO+SORT on Jetson TX2” | [IEEE Xplore record 9117960](https://ieeexplore.ieee.org/document/9117960) · fetch unavailable 2026-11-19 | Background for the PPT’s reported 97%/30 FPS benchmark target. | The paper could not be retrieved in this review. Verify title, authors, metric definition, dataset, hardware and publication before citation; it is not a Falcon result. |
| “Perimeter Intrusion Detection by Video Surveillance: A Survey” | [PMC9104546](https://pmc.ncbi.nlm.nih.gov/articles/PMC9104546/) · page accessible 2026-11-19 | Survey of perimeter-intrusion definitions, methods, datasets, and evaluation; highlights outdoor variability. | Use its evaluation framing; do not infer Falcon accuracy or security validation from a survey. |
| CCTV operator vigilance-decrement study | [ScienceDirect search for vigilance decrement](https://www.sciencedirect.com/search?qs=CCTV%20operator%20vigilance%20decrement) · exact article not confirmed | Source candidate for PPT’s 20–35 minute vigilance and ~50% detection statements. | Exact paper, population, task and limits were not supplied/verified; keep claims attributed to PPT until located. |
| IDSA CIBMS implementation/cost/rollout analysis | [IDSA/MP-IDSA site search](https://www.google.com/search?q=site%3Aidsa.in+CIBMS+implementation+challenges+cost+rollout) · exact source not confirmed | Context for deployment and program-level risks/costs. | Search result is not a citation; find the original report, author, date and pages before quoting. |
| MRFR Border Security Market report | [MRFR site search](https://www.google.com/search?q=site%3Awww.marketresearchfuture.com+border+security+market+43.82+76.52) · exact edition not confirmed | Potential source for PPT-37 market values. | Figures USD 43.82B/76.52B and other PPT market claims are PPT-sourced/unverified; validate report dates, scope and forecast. |
| BEL Border Surveillance System (BOSS) specification | [BEL site search](https://www.google.com/search?q=site%3Abel-india.in+Border+Surveillance+System+BOSS+specification) · exact primary document not confirmed | Public-system context and requirements for a fair comparison. | Do not state BOSS cannot retrofit or infer technical limits without an official source and deployment-specific scope. |

### Research evidence log

| Source | Checked | Result |
|---|---|---|
| Prototype URL `https://projecthailmary-auvpxb28z-mradulsingh109sprojects.vercel.app/` | 2026-11-19 | HTTP 404 via page fetch; no product behavior inferred. |
| Ultralytics guide | 2026-11-19 | Page fetched; current content describes a YOLO26 security alarm sample, email integration, and tracking. |
| IEEE record 9117960 | 2026-11-19 | Fetch did not provide paper content; bibliographic/metric details still need confirmation. |
| PMC9104546 | 2026-11-19 | Page fetched; article is a 2022 perimeter intrusion detection survey; cite the published page and its definitions. |
| Other references | 2026-11-19 | Exact report/article URLs were not present in the workspace or validated; search links above are discovery aids only, not primary citations. |

## PPT-46 competitor table — qualified comparison

| Dimension | CIBMS / BOSS | JARVIS by Staqu | FALCON plan / proof required |
|---|---|---|---|
| Stated category | PPT describes integrated border-surveillance system with intrusion and day/night thermal capability. | PPT describes AI video analytics/FRS on existing CCTV. | Software analytics layer over compatible existing CCTV; current repo contains a plan/schema, not a working deployed product. |
| Existing camera integration | PPT claims not retrofittable; **unverified** and potentially dependent on specific deployment. | PPT claims existing-CCTV support; **source not verified**. | Demonstrate ONVIF/RTSP on named devices and publish compatibility matrix (F2-02, F10-03, T2-02). |
| Edge/offline | Need official system architecture and site-specific details. | PPT alleges lack of edge-first zero-connectivity support; **unverified**. | Demonstrate local operation and reconnect sync in an isolated test; not yet implemented (F11-01, F13-04, T11-01). |
| Virtual fence/unfenced terrain | Compare only from official public specifications. | PPT alleges no software virtual fence for riverine terrain; **unverified**. | Demonstrate versioned lines/polygons and foot-point crossing; does not establish operational suitability for terrain (F4-01..04, T4-01..04). |
| Night/IR/thermal | PPT says intrusion plus day/night thermal imaging; confirm official specification. | PPT alleges no night/IR-specific model; **unverified**. | Requires compatible sensor and labeled test footage; feature remains planned/measurement-gated (F8-01..03, T8-01..03). |
| FRS metric | No matched metric supplied. | PPT claims 99.7% LFW; metric conditions/source not verified. | No Falcon accuracy claim; if FRS approved, publish FAR/FRR on governed data and human review (F7-01..04, T7-01..04). |
| Scope/interoperability | Do not compare procurement scope without official documents. | Do not infer integrations from marketing material. | Publish only tested adapters and APIs; mock C2 receiver is not a certified C2/C4I integration (F10-01..03, T10-01..03). |

## How Falcon plans to address claimed gaps

1. Reuse an existing CCTV feed through standard camera drivers, with a named tested-device matrix rather than “any camera” claim.
2. Keep inference and local alert/evidence functions on the edge; test the disconnected behavior and sync separately.
3. Use software-defined zone geometry with version history and operator review; outdoor geometry still needs calibration and site validation.
4. Add analytics through registry/plugin contracts only after compatible data, model license and acceptance tests exist.
5. Integrate with—not replace—existing C2/SOC through documented REST/webhook contracts and mocks first.

All comparative statements above require primary-source verification before a public submission. See tasks F0-05, F10-01..04, F13-02/03 and F15-04.

