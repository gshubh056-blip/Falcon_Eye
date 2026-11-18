# Dependency Graph and Critical Path

This graph is a dependency view, not a calendar. Task IDs and owners are in [01_IMPLEMENTATION_PLAN.md](./01_IMPLEMENTATION_PLAN.md) and [04_TASK_BOARD.csv](./04_TASK_BOARD.csv). Workstreams may parallelize only after the stated dependency is complete.

```mermaid
flowchart LR
  subgraph Foundation["P0 Foundation"]
    F001["F0-01 repo + paths"]
    F002["F0-02 pinned toolchain"]
    F003["F0-03 CI + secrets"]
    F004["F0-04 architecture ADR"]
    F005["F0-05 prototype/LUT review"]
    F006["F0-06 data/license plan"]
    F001 --> F002 --> F003
    F001 --> F004
    F001 --> F006
  end
  subgraph DataAPI["P1 Data and API"]
    D101["F1-01 schema validation"]
    D102["F1-02 migrations + seeds"]
    D103["F1-03 auth"]
    D104["F1-04 RBAC/site scope"]
    D105["F1-05 CRUD contracts"]
    D106["F1-06 audit/hash chain"]
    D107["F1-07 health/metrics"]
    D108["F1-08 users/roles + API gap decisions"]
    D101 --> D102 --> D103 --> D104 --> D105
    D104 --> D106
    D102 --> D107
    D105 --> D108
  end
  subgraph Capture["P2 Capture"]
    C201["F2-01 driver/file source"]
    C202["F2-02 RTSP/ONVIF"]
    C203["F2-03 reconnect/queue"]
    C204["F2-04 preprocess"]
    C201 --> C202
    C201 --> C203 --> C204
  end
  subgraph CV["P3 Detection/tracking"]
    V301["F3-01 detector"]
    V302["F3-02 tracker"]
    V303["F3-03 confirmation/persistence"]
    V304["F3-04 registry/export"]
    V301 --> V302 --> V303
    V301 --> V304
  end
  subgraph Vertical["P4 First vertical slice"]
    A401["F4-01 geometry"]
    A402["F4-02 fence config"]
    A403["F4-03 importer"]
    A404["F4-04 event rules"]
    A405["F4-05 alert state machine"]
    A406["F4-06 WS/broker"]
    A407["F4-07 webhook/siren"]
    A408["F4-08 evidence clip/snapshot"]
    A409["F4-09 event search/geo"]
    A401 --> A402 --> A404 --> A405 --> A406
    A401 --> A403
    A405 --> A407
    A404 --> A408
    A404 --> A409
  end
  subgraph Front["P9 Dashboard"]
    U901["F9-01 app shell"]
    U902["F9-02 auth/site"]
    U903["F9-03 live view"]
    U904["F9-04 alerts"]
    U905["F9-05 evidence"]
    U906["F9-06 GIS/admin"]
    U901 --> U902 --> U903 -->     U904 --> U905
    U902 --> U906
  end
  subgraph Release["P11-P15 Release"]
    S1101["F11-01 sync"]
    S1104["F11-04 deploy"]
    S1204["F12-04 verify ledger"]
    Q1301["F13-01 tests"]
    Q1302["F13-02 measures"]
    M1501["F15-01 demo"]
    M1503["F15-03 PPT audit"]
    S1101 --> S1104
    S1104 --> M1501
    S1204 --> Q1301
    U905 --> Q1301
    A404 --> Q1301
    Q1301 --> Q1302 --> M1503
    M1501 --> M1503
  end
  F003 --> D101
  F006 --> V301
  F002 --> C201
  D102 --> C203
  D105 --> A402
  D106 --> S1204
  D107 --> U906
  D108 --> U906
  C203 --> V301
  V303 --> A401
  A406 --> U903
  D103 --> U902
  A405 --> U904
  A408 --> U905
  A409 --> U905
  A404 --> S1101
  D102 --> S1204
```

## Critical path

`F0-01 → F2-01 → F2-03 → F3-01 → F3-02 → F3-03 → F4-01 → F4-02 → F4-04 → F4-05 → F4-06 → F9-03 → F13-03 → F15-03 → F15-05` (**118 person-hours** by current task estimates).

This longest dependency chain is calculated from `04_TASK_BOARD.csv`; it is not an elapsed-calendar forecast. Recalculate it whenever task dependencies or estimates change.

F0-06 (license/data review) can delay all real model inference; build only clearly labeled deterministic mock inference while that gate is unresolved. F1-01 requires actual PostgreSQL 16/TimescaleDB validation; static SQL inspection is not a substitute. F9-03 requires an actual media delivery path, not just an API mock.

## Parallel role lanes

| Lane | Can start after | Work | Integration contract |
|---|---|---|---|
| Backend | F0-01/F0-02 | Schema, migrations, auth/RBAC, CRUD, alert/evidence APIs, sync | Versioned OpenAPI; canonical PRD names/enums |
| CV-ML | F0-06 and detector input fixture | Preprocessing, detector/tracker adapters, geometry, rule plugins, benchmarks | Versioned frame/detection/track/event schemas; cached licensed weights |
| Frontend | F0-02 and WEB_FLOW/design review | App shell, auth, live, alerts, event/evidence, map/fence/admin | API mocks must match OpenAPI and are visibly test fixtures |
| DevOps | F0-01/F0-02 | CI, Compose, observability, packaging, offline cache, systemd | Health checks, version pins, explicit offline profile |
| QA | F0-03 and acceptance tests | Contract/fixtures, coverage, Playwright, robustness, metrics | Test IDs T0..T15 in task board; keep artifacts |
| Docs | Start immediately | Source decisions, training/privacy, operator runbooks, PPT traceability | No unsupported capability, market, legal or performance claims |

No lane may merge a mock as a real detector, silently broaden a role, or claim a hardware/protocol test that did not occur.
