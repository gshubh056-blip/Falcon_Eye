# FALCON Backend Entity Relationship Diagram

The ERD follows PRD/TRD canonical entity names. Hypertable entities are time-partitioned; relationships use composite `(id, timestamp)` references where required by TimescaleDB.

```mermaid
erDiagram
  ORGANIZATIONS ||--o{ SITES : owns
  SITES ||--o{ DEVICES : hosts
  SITES ||--o{ CAMERAS : operates
  DEVICES ||--o{ CAMERAS : processes
  CAMERAS ||--o{ ZONES : configures
  CAMERAS ||--o{ TRACKS : observes
  CAMERAS ||--o{ DETECTIONS : reports
  CAMERAS ||--o{ CAMERA_HEALTH : reports
  DEVICES ||--o{ HEALTH_METRICS : reports
  CAMERAS ||--o{ EVENTS : produces
  SITES ||--o{ EVENT_INDEX : scopes
  EVENT_INDEX ||--|| EVENTS : indexes
  EVENT_INDEX ||--o{ ALERTS : may_raise
  EVENT_INDEX ||--o{ EVIDENCE_FILES : preserves
  EVENT_INDEX ||--o{ MODEL_FEEDBACK : labels
  ALERTS ||--o{ ALERT_ACTIONS : records
  ALERTS ||--o{ ALERT_DELIVERIES : dispatches
  EVIDENCE_FILES ||--o{ EVIDENCE_ACCESS_LOG : accesses
  EVENT_INDEX ||--o{ LEDGER_ENTRIES : protects
  USERS ||--o{ ALERT_ACTIONS : performs
  USERS ||--o{ AUDIT_LOGS : acts
  USERS ||--o{ USER_ROLES : assigned
  ROLES ||--o{ USER_ROLES : grants
  USERS ||--o{ USER_SITE_ACCESS : scoped
  SITES ||--o{ USER_SITE_ACCESS : permits
  CAMERAS ||--o{ CAMERA_MODEL_ASSIGNMENTS : selects
  MODELS ||--o{ CAMERA_MODEL_ASSIGNMENTS : assigned
  CAMERAS ||--o{ CONFIGS : configures
  WATCHLIST_PLATES ||--o{ ANPR_READS : matches
  WATCHLIST_FACES ||--o{ FACE_EMBEDDINGS : enrolls
  WATCHLIST_FACES ||--o{ FACE_MATCHES : candidate
  CAMERAS ||--o{ ANPR_READS : reads
  CAMERAS ||--o{ FACE_MATCHES : observes
  DEVICES ||--o{ SYNC_QUEUE : forwards
  WEBHOOK_ENDPOINTS ||--o{ WEBHOOK_DELIVERIES : receives
  LEDGER_BLOCKS ||--o{ LEDGER_ENTRIES : anchors
```

## Time-series partition keys

| Table | Partition column | Primary key |
|---|---|---|
| `events` | `captured_at` | `(id, captured_at)` |
| `detections` | `detected_at` | `(id, detected_at)` |
| `camera_health` | `sampled_at` | `(camera_id, sampled_at)` |
| `health_metrics` | `sampled_at` | `(device_id, metric_name, sampled_at)` |
| `anpr_reads` | `read_at` | `(id, read_at)` |
| `face_matches` | `matched_at` | `(id, matched_at)` |

`event_index` is the ordinary relational identity/retention row for a time-series event. Alerts/evidence/ledger reference it so the event hypertable can expire chunks without inbound foreign keys blocking chunk removal. The event writer inserts the index and hypertable row in one transaction. A retention worker removes dependent relational records only after checking their own retention and legal-hold policy. `alerts`, evidence metadata, ledger entries, watchlists and audit entities remain ordinary relational tables.
