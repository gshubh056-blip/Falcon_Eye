# Dataset and Annotation Plan

No weights, datasets, or operational footage are committed to this repository.
Approved assets require license review, checksums, labels, purpose, and retention
rules before acquisition.

| Asset family | Required review | Label/quality gate | Status |
|---|---|---|---|
| Person/vehicle detection | License, provenance, permitted use | Named classes, train/validation separation | Not acquired |
| ANPR | Jurisdiction, authorization, retention | Plate classes or OCR labels, reject/unknown policy | Gated |
| Face recognition | Legal basis, consent/privacy review | Controlled watchlist, FAR/FRR, human review | Disabled |
| IR/thermal | Sensor compatibility and license | Day/night/thermal calibration, metadata | Not acquired |
| Synthetic demo media | Locally generated and clearly labeled | No real person or camera identity | Planned |

## Candidate review: TRD YOLOv8s

Reviewed 2026-11-19; **not approved for download or use**.

- The [Ultralytics YOLOv8 documentation](https://docs.ultralytics.com/models/yolov8/)
  states that YOLOv8 models are offered under AGPL-3.0 or an Enterprise license.
- The [Ultralytics license page](https://www.ultralytics.com/license) says the
  Enterprise license is required for proprietary/closed-source, commercial,
  customer-facing, SaaS, or embedded use that is not released under AGPL-3.0.
- This repository has no root project license file, so an AGPL compatibility
  decision cannot be inferred. The project owner must choose the project's
  licensing direction or provide an applicable Enterprise license.
- The YOLOv8 documentation describes COCO-pretrained models. The
  [COCO terms](https://cocodataset.org/dataset/termsofuse.htm) license its
  annotations under CC-BY-4.0, but state that image copyright remains with
  underlying owners and use must follow the images' Flickr terms. Asset-level
  training-data provenance and permitted-use review remains outstanding.

No model package or weights were downloaded. Do not enable inference until the
project license decision and model/data provenance review are recorded.

**Recommended direction:** evaluate an alternative whose implementation,
weights, and training-data provenance have separately documented terms, rather
than introducing unresolved AGPL obligations. No alternative is approved yet;
do not treat this recommendation as permission to download or deploy a model.

The dashboard may use an in-browser COCO-SSD demo for interface validation only.
It must remain labeled as demo inference, must not be used for security decisions,
and must not be represented as an approved FALCON detector. The approved model
registry, license, provenance, benchmark, and rollback gates still apply.
