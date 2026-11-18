# FALCON Guide Conflict Register

The implementation guide follows the PRD/TRD for product requirements, repository paths, names, protocols and versions. Differences introduced by later implementation prompts are recorded below rather than silently changing the project contract.

| Area | Resolution |
|---|---|
| Live capture | GStreamer/OpenCV capture; FFmpeg only for evidence encoding |
| Default tracker | ByteTrack; DeepSORT is selectable |
| Default OCR | PaddleOCR; EasyOCR fallback |
| Face embedding | 512-D ArcFace/InsightFace |
| Evidence ledger | P0 local hash chain and Ed25519; P1 Merkle; P2 Fabric |
| Message fan-out | Redis Streams for MVP queue; MQTT for alerts/SOC; never duplicate by default |
| Python version | TRD pins Python 3.12.9; the later backend master prompt asks for Python 3.11. Keep TRD version unless the team formally revises and tests the baseline. |
| Role and alert enums | PRD roles and severity/state values prevail over the later prompt's alternate role names and `INVESTIGATING` state. Add mappings only through an approved API contract. |
| Database names | TRD/PRD table names are canonical. Backend-specific supplementary tables are allowed when they do not rename or weaken those contracts. |
| Timescale event keys | PRD sample DDL declares a single-column primary key on `events` and then makes it a hypertable by `captured_at`. Timescale unique constraints on a hypertable must include its partition key. `db/schema.sql` uses `(id, captured_at)` and matching composite references for time-series entities. |
| UUID generation | TRD requires `gen_random_uuid()`. UUIDv7 in the later prompt is not enabled without a supported PostgreSQL extension; ordered sync uses an explicit per-node sequence and idempotency key. |
| Offline evidence | Edge-local operation is authoritative during WAN loss; sync is idempotent store-and-forward. The browser does not claim queued mutations will execute unless the backend confirms durable queue acceptance. |
