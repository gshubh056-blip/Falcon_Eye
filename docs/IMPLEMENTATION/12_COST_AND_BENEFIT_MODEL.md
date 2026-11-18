# Cost and Benefit Model

This is a fillable calculation model, not a quotation or ROI claim. No local hardware quotes, energy bills, camera counts, storage measurements, or staffing baselines were found in the repository. Every input must be marked **ASSUMPTION**, **QUOTE**, **MEASURED**, or **PPT-SOURCED / UNVERIFIED**, with source/date/owner.

## Editable inputs

| Variable | Unit | Value | Evidence required |
|---|---|---|---|
| `N_sites` | sites | ______ | Deployment inventory |
| `N_cameras_per_site` | cameras | ______ | Camera inventory and supported-profile matrix |
| `C_edge_node` | local currency / site | ______ | At least one dated NUC/Jetson quote with GPU/accelerator and warranty |
| `C_install_per_site` | local currency | ______ | Site survey, cabling, commissioning, travel quote |
| `C_storage_per_site` | local currency | ______ | Disk/object retention sizing and quote |
| `C_network_per_site` | local currency / year | ______ | Actual link plan and usage billing |
| `W_edge` | watts | ______ | Meter or exact device/vendor spec |
| `H_operation_per_day` | hours | ______ | Actual duty schedule |
| `P_energy` | local currency / kWh | ______ | Applicable tariff/date |
| `H_support_per_month` | hours | ______ | Staff roster/support model |
| `C_staff_hour` | local currency / hour | ______ | Approved loaded labor rate |
| `R_evidence_GB_per_camera_day` | GB | ______ | Measured clips/snapshots retention profile |
| `D_retention` | days | ______ | PRD policy/deployment legal approval |
| `Q_edge` | bytes sent / camera / day | ______ | Measured sync under declared profile |
| `Q_cloud_baseline` | bytes sent / camera / day | ______ | Matched cloud-only baseline |
| `C_smart_camera` | local currency / camera | ______ | Comparable dated vendor quote including installation |
| `C_cloud_video` | local currency / camera-month | ______ | Comparable storage, egress, inference and retention quote |
| `T_years` | years | ______ | Finance-approved comparison horizon |
| `M_maintenance` | local currency / year | ______ | Support, spares, patching and replacement estimate |

## Formula sheet

| Measure | Formula | Interpretation |
|---|---|---|
| Edge initial CapEx | `N_sites × (C_edge_node + C_storage_per_site + C_install_per_site)` | Edge node/site setup; camera reuse savings are separate |
| Edge annual energy | `N_sites × W_edge/1000 × H_operation_per_day × 365 × P_energy` | Add cooling/UPS where measured |
| Edge annual OpEx | `energy + network + support labor + maintenance + storage replacement` | Separate one-time and recurring costs |
| Edge TCO | `edge CapEx + T_years × edge annual OpEx` | No discounting unless finance provides discount rate |
| Smart-camera CapEx baseline | `N_sites × N_cameras_per_site × (C_smart_camera + install_per_camera)` | Comparable scope/quality required |
| Cloud-only TCO | `N_cameras × T_years × (C_cloud_video + storage + egress + support)` | Include cloud inference, retention, bandwidth and vendor fees |
| Break-even / ROI | `(baseline TCO − Falcon TCO) / Falcon TCO` | Calculate only with comparable quotes and stated horizon |
| Bandwidth reduction | `1 − (Q_edge / Q_cloud_baseline)` | Must use identical content duration, quality and evidence policy |
| Cost per camera-year | `TCO / (N_cameras × T_years)` | Report with hardware, retention, sites and labor assumptions |

Do not count avoided staff as cash savings without an approved staffing model. Report capacity/time reallocated as operational benefit, distinct from financial ROI. Do not compare lower-resolution evidence to a higher-quality cloud baseline without disclosing the quality difference.

## Sensitivity scenarios

Compute low/base/high scenarios by varying only named inputs (camera count, stream bitrate, days retained, clip frequency, link price, node cost, support hours, energy). Each scenario must preserve the same functional and evidentiary requirements. Keep original input sheet and formulas so a reviewer can reproduce results.

| Scenario | Edge node/camera load | Retention and clip policy | Network price | Support/maintenance | Result |
|---|---|---|---|---|---|
| Low | ASSUMPTION: ______ | ASSUMPTION: ______ | ASSUMPTION: ______ | ASSUMPTION: ______ | Calculate after quotes |
| Base | ASSUMPTION: ______ | ASSUMPTION: ______ | ASSUMPTION: ______ | ASSUMPTION: ______ | Calculate after quotes |
| High | ASSUMPTION: ______ | ASSUMPTION: ______ | ASSUMPTION: ______ | ASSUMPTION: ______ | Calculate after quotes |

The blanks are named input cells with a required evidence owner, not project facts. Populate them before presenting a cost conclusion.

## PPT market figures (not validated)

The following are reproduced only as claims attributed through the PPT to MRFR; exact report editions, source pages, methodology and access dates were not supplied in the workspace. Do not present them as verified market facts until [14_REFERENCES_AND_COMPETITIVE_ANALYSIS.md](./14_REFERENCES_AND_COMPETITIVE_ANALYSIS.md) completes source verification.

| PPT claim | Status now | Required action |
|---|---|---|
| Border security spend USD 43.82B (2026) → USD 76.52B (2035) | PPT-SOURCED / UNVERIFIED | Find exact MRFR report, definition, currency/year, publication date and source URL; verify arithmetic/forecast |
| Video-analytics market USD 14.65B → USD 41.39B (2026–2031) | PPT-SOURCED / UNVERIFIED | Verify report title, market definition, base/forecast years and original table |
| Perimeter/intrusion detection is a leading segment | PPT-SOURCED / UNVERIFIED | Verify segment ranking and exact wording/source |
| Asia-Pacific video analytics CAGR 24.4% | PPT-SOURCED / UNVERIFIED | Verify region, interval and report edition |
| Facial recognition fastest-growing service CAGR 24.3% | PPT-SOURCED / UNVERIFIED | Verify service taxonomy, interval and source |

## Required review

Before sharing this model, Finance/Team lead confirms inputs and comparability; QA confirms measured bandwidth/retention; DevOps confirms power/storage specs; Docs captures source URLs and date. Until then, no numeric Falcon cost, ROI, TCO, CapEx, OpEx, or bandwidth savings claim is approved.

