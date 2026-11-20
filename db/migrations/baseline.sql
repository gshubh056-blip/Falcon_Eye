-- FALCON baseline schema for PostgreSQL 16 and compatible TimescaleDB.
-- Apply once to a clean database using a privileged migration role.
-- Application credentials must not own these tables or bypass append-only guards.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS timescaledb;

DO $$ BEGIN
  CREATE TYPE falcon_severity AS ENUM ('info', 'low', 'medium', 'high', 'critical');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE falcon_alert_status AS ENUM (
    'new', 'acknowledged', 'escalated', 'resolved', 'false_positive', 'closed'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE falcon_camera_type AS ENUM ('visible', 'ir', 'thermal');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE falcon_zone_type AS ENUM ('line', 'polygon');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE falcon_zone_direction AS ENUM ('a_to_b', 'b_to_a', 'both');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE falcon_evidence_kind AS ENUM ('snapshot', 'clip', 'manifest');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE OR REPLACE FUNCTION falcon_set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION falcon_reject_immutable_change()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION 'table % is append-only', TG_TABLE_NAME
    USING ERRCODE = '55000';
END;
$$;

CREATE TABLE IF NOT EXISTS organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  code TEXT NOT NULL UNIQUE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  code TEXT NOT NULL UNIQUE,
  site_type TEXT NOT NULL DEFAULT 'bop',
  sector TEXT,
  latitude NUMERIC(9, 6) CHECK (latitude BETWEEN -90 AND 90),
  longitude NUMERIC(9, 6) CHECK (longitude BETWEEN -180 AND 180),
  timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata',
  edge_node_id UUID,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id UUID NOT NULL REFERENCES sites(id),
  hostname TEXT NOT NULL,
  hardware_profile TEXT NOT NULL,
  software_version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'offline'
    CHECK (status IN ('online', 'offline', 'degraded', 'maintenance')),
  secure_boot BOOLEAN NOT NULL DEFAULT FALSE,
  disk_encrypted BOOLEAN NOT NULL DEFAULT FALSE,
  last_seen TIMESTAMPTZ,
  last_sync_cursor TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (site_id, hostname)
);

ALTER TABLE sites
  ADD CONSTRAINT fk_sites_edge_node
  FOREIGN KEY (edge_node_id) REFERENCES devices(id)
  DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE IF NOT EXISTS cameras (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id UUID NOT NULL REFERENCES sites(id),
  device_id UUID REFERENCES devices(id),
  name TEXT NOT NULL,
  protocol TEXT NOT NULL DEFAULT 'rtsp'
    CHECK (protocol IN ('rtsp', 'rtsps', 'onvif', 'file', 'webcam')),
  stream_uri TEXT,
  stream_uri_ciphertext BYTEA,
  credential_ref TEXT,
  onvif_host TEXT,
  onvif_port INTEGER CHECK (onvif_port BETWEEN 1 AND 65535),
  onvif_profile TEXT,
  camera_type falcon_camera_type NOT NULL DEFAULT 'visible',
  mode TEXT NOT NULL DEFAULT 'auto' CHECK (mode IN ('day', 'night', 'auto')),
  latitude NUMERIC(9, 6) CHECK (latitude BETWEEN -90 AND 90),
  longitude NUMERIC(9, 6) CHECK (longitude BETWEEN -180 AND 180),
  heading_degrees NUMERIC(6, 2) CHECK (heading_degrees >= 0 AND heading_degrees < 360),
  mounting_height_m NUMERIC(7, 2) CHECK (mounting_height_m > 0),
  lens_info JSONB NOT NULL DEFAULT '{}'::jsonb,
  fps_target NUMERIC(5, 2) NOT NULL DEFAULT 12 CHECK (fps_target > 0 AND fps_target <= 60),
  ptz_capable BOOLEAN NOT NULL DEFAULT FALSE,
  status TEXT NOT NULL DEFAULT 'disconnected'
    CHECK (status IN ('connected', 'disconnected', 'degraded', 'disabled')),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  config JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (site_id, name)
);

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  email TEXT,
  password_hash TEXT,
  mfa_required BOOLEAN NOT NULL DEFAULT TRUE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (password_hash IS NULL OR length(password_hash) >= 20)
);

CREATE TABLE IF NOT EXISTS roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  permissions JSONB NOT NULL DEFAULT '{}'::jsonb,
  system_role BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(permissions) = 'object')
);

INSERT INTO roles (name, permissions) VALUES
  ('operator', '{}'::jsonb),
  ('supervisor', '{}'::jsonb),
  ('analyst', '{}'::jsonb),
  ('admin', '{}'::jsonb),
  ('ml_maintainer', '{}'::jsonb),
  ('auditor', '{}'::jsonb),
  ('api_integration', '{}'::jsonb)
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS user_roles (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id),
  assigned_by UUID REFERENCES users(id),
  assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS user_site_access (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  site_id UUID NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
  granted_by UUID REFERENCES users(id),
  granted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, site_id)
);

CREATE TABLE IF NOT EXISTS auth_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  refresh_token_sha256 CHAR(64) NOT NULL UNIQUE,
  issued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at TIMESTAMPTZ NOT NULL,
  revoked_at TIMESTAMPTZ,
  last_used_at TIMESTAMPTZ,
  source_ip INET,
  user_agent TEXT,
  CHECK (expires_at > issued_at)
);

CREATE INDEX IF NOT EXISTS idx_auth_sessions_user_expiry
  ON auth_sessions (user_id, expires_at DESC)
  WHERE revoked_at IS NULL;

CREATE TABLE IF NOT EXISTS api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  token_sha256 CHAR(64) NOT NULL UNIQUE,
  role_id UUID NOT NULL REFERENCES roles(id),
  site_id UUID REFERENCES sites(id),
  created_by UUID REFERENCES users(id),
  expires_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS zones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  camera_id UUID NOT NULL REFERENCES cameras(id),
  name TEXT NOT NULL,
  geometry_type falcon_zone_type NOT NULL,
  points JSONB NOT NULL,
  direction falcon_zone_direction NOT NULL DEFAULT 'both',
  classes_allowed TEXT[] NOT NULL DEFAULT ARRAY['person', 'vehicle']::TEXT[],
  severity falcon_severity NOT NULL DEFAULT 'high',
  schedule JSONB NOT NULL DEFAULT '{"all_day": true}'::jsonb,
  calibration JSONB NOT NULL DEFAULT '{}'::jsonb,
  source TEXT NOT NULL DEFAULT 'manual'
    CHECK (source IN ('manual', 'roboflow')),
  version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
  active BOOLEAN NOT NULL DEFAULT FALSE,
  effective_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  retired_at TIMESTAMPTZ,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(points) = 'array'),
  CHECK (jsonb_typeof(schedule) = 'object'),
  UNIQUE (camera_id, name, version)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_zones_one_active_version
  ON zones (camera_id, name) WHERE active;

CREATE TABLE IF NOT EXISTS models (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  task TEXT NOT NULL
    CHECK (task IN ('person_vehicle', 'face', 'plate', 'ir_thermal', 'fence_zone', 'other')),
  version TEXT NOT NULL,
  architecture TEXT NOT NULL,
  format TEXT NOT NULL CHECK (format IN ('pt', 'onnx', 'engine')),
  licence TEXT NOT NULL,
  artifact_uri TEXT NOT NULL,
  artifact_sha256 CHAR(64) NOT NULL
    CHECK (artifact_sha256 ~ '^[0-9a-f]{64}$'),
  dataset_hash CHAR(64),
  test_report JSONB NOT NULL DEFAULT '{}'::jsonb,
  metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  signature BYTEA,
  status TEXT NOT NULL DEFAULT 'registered'
    CHECK (status IN ('registered', 'verified', 'staged', 'active', 'rejected', 'retired')),
  active BOOLEAN NOT NULL DEFAULT FALSE,
  signed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (name, version)
);

CREATE TABLE IF NOT EXISTS camera_model_assignments (
  camera_id UUID NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
  model_id UUID NOT NULL REFERENCES models(id),
  task TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT FALSE,
  assigned_by UUID REFERENCES users(id),
  assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (camera_id, task, model_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_camera_active_model_task
  ON camera_model_assignments (camera_id, task) WHERE active;

CREATE TABLE IF NOT EXISTS configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  camera_id UUID REFERENCES cameras(id),
  zone_id UUID REFERENCES zones(id),
  revision INTEGER NOT NULL CHECK (revision > 0),
  body JSONB NOT NULL,
  approved_by UUID REFERENCES users(id),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(body) = 'object'),
  UNIQUE (camera_id, zone_id, revision)
);

CREATE TABLE IF NOT EXISTS alert_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  event_type TEXT NOT NULL,
  site_id UUID REFERENCES sites(id),
  camera_id UUID REFERENCES cameras(id),
  params JSONB NOT NULL DEFAULT '{}'::jsonb,
  severity falcon_severity NOT NULL,
  cooldown_seconds INTEGER NOT NULL DEFAULT 30
    CHECK (cooldown_seconds BETWEEN 5 AND 3600),
  escalation_seconds INTEGER CHECK (escalation_seconds > 0),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(params) = 'object')
);

CREATE TABLE IF NOT EXISTS tracks (
  camera_id UUID NOT NULL REFERENCES cameras(id),
  track_id TEXT NOT NULL,
  object_class TEXT NOT NULL CHECK (object_class IN ('person', 'vehicle')),
  status TEXT NOT NULL CHECK (status IN ('tentative', 'confirmed', 'lost', 'expired')),
  first_seen TIMESTAMPTZ NOT NULL,
  last_seen TIMESTAMPTZ NOT NULL,
  trajectory JSONB NOT NULL DEFAULT '[]'::jsonb,
  avg_speed_mps DOUBLE PRECISION CHECK (avg_speed_mps >= 0),
  reid_embedding_ref TEXT,
  model_id UUID REFERENCES models(id),
  PRIMARY KEY (camera_id, track_id),
  CHECK (last_seen >= first_seen),
  CHECK (jsonb_typeof(trajectory) = 'array')
);

-- A small relational identity row lets alerts/evidence reference an event while
-- the event payload itself lives in a Timescale hypertable with timed retention.
CREATE TABLE IF NOT EXISTS event_index (
  id UUID NOT NULL,
  captured_at TIMESTAMPTZ NOT NULL,
  node_id UUID NOT NULL REFERENCES devices(id),
  camera_id UUID NOT NULL REFERENCES cameras(id),
  site_id UUID NOT NULL REFERENCES sites(id),
  legal_hold BOOLEAN NOT NULL DEFAULT FALSE,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, captured_at)
);

CREATE INDEX IF NOT EXISTS idx_event_index_retention
  ON event_index (expires_at) WHERE legal_hold = FALSE;

CREATE TABLE IF NOT EXISTS events (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  node_id UUID NOT NULL REFERENCES devices(id),
  camera_id UUID NOT NULL REFERENCES cameras(id),
  site_id UUID NOT NULL REFERENCES sites(id),
  zone_id UUID REFERENCES zones(id),
  track_id TEXT,
  category TEXT NOT NULL,
  object_class TEXT,
  severity falcon_severity NOT NULL DEFAULT 'info',
  status TEXT NOT NULL DEFAULT 'recorded'
    CHECK (status IN ('recorded', 'alerted', 'false_positive')),
  confidence REAL CHECK (confidence BETWEEN 0 AND 1),
  explanation JSONB NOT NULL DEFAULT '{}'::jsonb,
  rule_id TEXT,
  rule_version INTEGER,
  model_id UUID REFERENCES models(id),
  bbox JSONB,
  latitude NUMERIC(9, 6) CHECK (latitude BETWEEN -90 AND 90),
  longitude NUMERIC(9, 6) CHECK (longitude BETWEEN -180 AND 180),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  captured_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, captured_at),
  FOREIGN KEY (id, captured_at)
    REFERENCES event_index(id, captured_at) DEFERRABLE INITIALLY DEFERRED,
  CHECK (jsonb_typeof(explanation) = 'object'),
  CHECK (jsonb_typeof(metadata) = 'object'),
  CHECK (bbox IS NULL OR jsonb_typeof(bbox) = 'array')
);

SELECT create_hypertable(
  'events', 'captured_at', if_not_exists => TRUE
);

CREATE INDEX IF NOT EXISTS idx_events_camera_time
  ON events (camera_id, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_site_type_time
  ON events (site_id, category, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_severity_time
  ON events (severity, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_metadata_gin
  ON events USING GIN (metadata);

CREATE TABLE IF NOT EXISTS detections (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  event_id UUID,
  event_captured_at TIMESTAMPTZ,
  camera_id UUID NOT NULL REFERENCES cameras(id),
  track_id TEXT,
  object_class TEXT NOT NULL CHECK (object_class IN ('person', 'vehicle')),
  confidence REAL NOT NULL CHECK (confidence BETWEEN 0 AND 1),
  bbox JSONB NOT NULL,
  frame_id TEXT NOT NULL,
  model_id UUID REFERENCES models(id),
  mode TEXT NOT NULL DEFAULT 'day' CHECK (mode IN ('day', 'night')),
  detected_at TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id, detected_at),
  CHECK (jsonb_typeof(bbox) = 'array'),
  CHECK ((event_id IS NULL) = (event_captured_at IS NULL)),
  FOREIGN KEY (camera_id, track_id) REFERENCES tracks(camera_id, track_id)
);

SELECT create_hypertable('detections', 'detected_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_detections_camera_time
  ON detections (camera_id, detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_detections_track_time
  ON detections (camera_id, track_id, detected_at DESC);

CREATE TABLE IF NOT EXISTS alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL,
  event_captured_at TIMESTAMPTZ NOT NULL,
  category TEXT NOT NULL,
  severity falcon_severity NOT NULL,
  status falcon_alert_status NOT NULL DEFAULT 'new',
  assigned_to UUID REFERENCES users(id),
  acknowledged_by UUID REFERENCES users(id),
  acknowledged_at TIMESTAMPTZ,
  resolved_at TIMESTAMPTZ,
  false_positive BOOLEAN NOT NULL DEFAULT FALSE,
  false_positive_reason TEXT,
  escalation_level SMALLINT NOT NULL DEFAULT 0 CHECK (escalation_level >= 0),
  escalated_at TIMESTAMPTZ,
  cooldown_until TIMESTAMPTZ,
  dedupe_key TEXT NOT NULL UNIQUE,
  idempotency_key TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (event_id, event_captured_at)
    REFERENCES event_index(id, captured_at) DEFERRABLE INITIALLY DEFERRED,
  CHECK (status <> 'false_positive' OR false_positive),
  CHECK (
    status <> 'false_positive'
    OR (false_positive_reason IS NOT NULL AND length(trim(false_positive_reason)) > 0)
  )
);

CREATE INDEX IF NOT EXISTS idx_alert_status_severity_time
  ON alerts (status, severity, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alert_assignee_status
  ON alerts (assigned_to, status, created_at DESC);

CREATE TABLE IF NOT EXISTS alert_actions (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  alert_id UUID NOT NULL REFERENCES alerts(id),
  actor_id UUID REFERENCES users(id),
  action TEXT NOT NULL
    CHECK (action IN ('acknowledge', 'assign', 'escalate', 'resolve', 'false_positive', 'close')),
  reason TEXT,
  previous_status falcon_alert_status,
  new_status falcon_alert_status,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  acted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(details) = 'object'),
  CHECK (action <> 'false_positive' OR length(trim(reason)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_alert_actions_alert_time
  ON alert_actions (alert_id, acted_at);

CREATE TABLE IF NOT EXISTS alert_deliveries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  alert_id UUID NOT NULL REFERENCES alerts(id),
  channel TEXT NOT NULL CHECK (channel IN ('websocket', 'mqtt', 'redis', 'webhook', 'siren')),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'delivered', 'retrying', 'failed', 'dead_letter')),
  attempts SMALLINT NOT NULL DEFAULT 0 CHECK (attempts >= 0),
  last_error TEXT,
  next_attempt_at TIMESTAMPTZ,
  delivered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS watchlist_plates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  normalized_plate TEXT NOT NULL,
  jurisdiction TEXT,
  category TEXT NOT NULL
    CHECK (category IN ('stolen', 'wanted', 'blacklisted', 'whitelisted')),
  reason TEXT NOT NULL,
  added_by UUID REFERENCES users(id),
  approved_by UUID REFERENCES users(id),
  expiry_at TIMESTAMPTZ NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (normalized_plate, category)
);

CREATE TABLE IF NOT EXISTS anpr_reads (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  camera_id UUID NOT NULL REFERENCES cameras(id),
  site_id UUID NOT NULL REFERENCES sites(id),
  watchlist_plate_id UUID REFERENCES watchlist_plates(id),
  plate_text TEXT NOT NULL,
  per_char_conf JSONB NOT NULL DEFAULT '[]'::jsonb,
  overall_conf REAL NOT NULL CHECK (overall_conf BETWEEN 0 AND 1),
  state_code TEXT,
  format_valid BOOLEAN NOT NULL DEFAULT FALSE,
  vehicle_type TEXT,
  direction TEXT CHECK (direction IN ('entry', 'exit', 'unknown')),
  plate_crop_uri TEXT,
  vehicle_snapshot_uri TEXT,
  fused_from_frames SMALLINT NOT NULL DEFAULT 1
    CHECK (fused_from_frames BETWEEN 1 AND 5),
  stage_latency_ms JSONB NOT NULL DEFAULT '{}'::jsonb,
  read_at TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id, read_at),
  CHECK (jsonb_typeof(per_char_conf) = 'array'),
  CHECK (jsonb_typeof(stage_latency_ms) = 'object')
);

SELECT create_hypertable('anpr_reads', 'read_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_anpr_site_time ON anpr_reads (site_id, read_at DESC);
CREATE INDEX IF NOT EXISTS idx_anpr_plate_time ON anpr_reads (plate_text, read_at DESC);

CREATE TABLE IF NOT EXISTS watchlist_faces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_label TEXT NOT NULL,
  legal_basis TEXT NOT NULL,
  consent_ref TEXT,
  category TEXT NOT NULL,
  reason TEXT NOT NULL,
  expiry_at TIMESTAMPTZ NOT NULL,
  added_by UUID REFERENCES users(id),
  approved_by UUID REFERENCES users(id),
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS face_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  watchlist_face_id UUID NOT NULL REFERENCES watchlist_faces(id) ON DELETE CASCADE,
  embedding_ciphertext BYTEA NOT NULL,
  encryption_key_ref TEXT NOT NULL,
  embedding_dim SMALLINT NOT NULL DEFAULT 512 CHECK (embedding_dim = 512),
  quality REAL NOT NULL CHECK (quality BETWEEN 0 AND 1),
  faiss_index_id TEXT,
  source TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS face_matches (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  camera_id UUID NOT NULL REFERENCES cameras(id),
  site_id UUID NOT NULL REFERENCES sites(id),
  watchlist_face_id UUID REFERENCES watchlist_faces(id),
  similarity REAL NOT NULL CHECK (similarity BETWEEN 0 AND 1),
  confidence REAL NOT NULL CHECK (confidence BETWEEN 0 AND 1),
  quality REAL NOT NULL CHECK (quality BETWEEN 0 AND 1),
  face_crop_uri TEXT,
  purpose TEXT NOT NULL,
  human_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
  human_decision TEXT CHECK (human_decision IN ('confirmed', 'rejected', 'unsure')),
  reviewed_by UUID REFERENCES users(id),
  reviewed_at TIMESTAMPTZ,
  matched_at TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id, matched_at),
  CHECK (
    (human_decision IS NULL AND NOT human_confirmed)
    OR (human_decision = 'confirmed' AND human_confirmed)
    OR (human_decision IN ('rejected', 'unsure') AND NOT human_confirmed)
  ),
  CHECK (
    human_decision IS NULL
    OR (reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL)
  )
);

SELECT create_hypertable('face_matches', 'matched_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_face_matches_site_time
  ON face_matches (site_id, matched_at DESC);

CREATE TABLE IF NOT EXISTS evidence_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL,
  event_captured_at TIMESTAMPTZ NOT NULL,
  kind falcon_evidence_kind NOT NULL,
  object_key TEXT NOT NULL UNIQUE,
  sha256 CHAR(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
  size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
  encrypted BOOLEAN NOT NULL DEFAULT TRUE,
  encryption_key_id TEXT,
  retention_until TIMESTAMPTZ,
  legal_hold BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (event_id, event_captured_at)
    REFERENCES event_index(id, captured_at) DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS idx_evidence_event
  ON evidence_files (event_id, event_captured_at);
CREATE INDEX IF NOT EXISTS idx_evidence_retention
  ON evidence_files (retention_until) WHERE legal_hold = FALSE;

CREATE TABLE IF NOT EXISTS evidence_access_log (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  evidence_id UUID NOT NULL REFERENCES evidence_files(id),
  user_id UUID REFERENCES users(id),
  action TEXT NOT NULL CHECK (action IN ('view', 'download', 'verify', 'export')),
  purpose TEXT,
  ip_address INET,
  accessed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ledger_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL,
  event_captured_at TIMESTAMPTZ NOT NULL,
  evidence_sha256 CHAR(64) NOT NULL CHECK (evidence_sha256 ~ '^[0-9a-f]{64}$'),
  metadata_sha256 CHAR(64) NOT NULL CHECK (metadata_sha256 ~ '^[0-9a-f]{64}$'),
  prev_hash CHAR(64) CHECK (prev_hash IS NULL OR prev_hash ~ '^[0-9a-f]{64}$'),
  entry_hash CHAR(64) NOT NULL UNIQUE CHECK (entry_hash ~ '^[0-9a-f]{64}$'),
  ed25519_signature BYTEA NOT NULL,
  signer_node_id UUID NOT NULL REFERENCES devices(id),
  merkle_root CHAR(64),
  anchor_status TEXT NOT NULL DEFAULT 'pending'
    CHECK (anchor_status IN ('pending', 'anchored', 'failed', 'not_configured')),
  anchored_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (event_id, event_captured_at)
    REFERENCES event_index(id, captured_at) DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS idx_ledger_event_time
  ON ledger_entries (event_id, event_captured_at);

CREATE TABLE IF NOT EXISTS ledger_blocks (
  block_height BIGINT PRIMARY KEY CHECK (block_height > 0),
  merkle_root CHAR(64) NOT NULL CHECK (merkle_root ~ '^[0-9a-f]{64}$'),
  prev_block_hash CHAR(64),
  entries_count INTEGER NOT NULL CHECK (entries_count > 0),
  signature BYTEA NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  actor_id UUID REFERENCES users(id),
  action TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id TEXT,
  purpose TEXT,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  ip_address INET,
  request_id UUID,
  prev_hash CHAR(64),
  entry_hash CHAR(64) NOT NULL UNIQUE CHECK (entry_hash ~ '^[0-9a-f]{64}$'),
  CHECK (prev_hash IS NULL OR prev_hash ~ '^[0-9a-f]{64}$'),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(details) = 'object')
);

CREATE INDEX IF NOT EXISTS idx_audit_resource_time
  ON audit_logs (resource_type, resource_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_actor_time
  ON audit_logs (actor_id, created_at DESC);

CREATE TABLE IF NOT EXISTS health_metrics (
  device_id UUID NOT NULL REFERENCES devices(id),
  camera_id UUID REFERENCES cameras(id),
  metric_name TEXT NOT NULL,
  metric_value DOUBLE PRECISION NOT NULL,
  unit TEXT,
  status TEXT,
  sampled_at TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (device_id, metric_name, sampled_at)
);

SELECT create_hypertable('health_metrics', 'sampled_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_health_device_time
  ON health_metrics (device_id, sampled_at DESC);

CREATE TABLE IF NOT EXISTS camera_health (
  camera_id UUID NOT NULL REFERENCES cameras(id),
  sampled_at TIMESTAMPTZ NOT NULL,
  fps REAL CHECK (fps >= 0),
  latency_ms REAL CHECK (latency_ms >= 0),
  dropped_frames BIGINT NOT NULL DEFAULT 0 CHECK (dropped_frames >= 0),
  reconnect_count BIGINT NOT NULL DEFAULT 0 CHECK (reconnect_count >= 0),
  status TEXT NOT NULL,
  PRIMARY KEY (camera_id, sampled_at)
);

SELECT create_hypertable('camera_health', 'sampled_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_camera_health_time
  ON camera_health (camera_id, sampled_at DESC);

CREATE TABLE IF NOT EXISTS sync_queue (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  idempotency_key TEXT NOT NULL UNIQUE,
  source_node_id UUID NOT NULL REFERENCES devices(id),
  event_sequence BIGINT NOT NULL CHECK (event_sequence > 0),
  payload_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'in_progress', 'synced', 'conflict', 'dead_letter')),
  attempt_count SMALLINT NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  next_attempt_at TIMESTAMPTZ,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (source_node_id, event_sequence),
  CHECK (jsonb_typeof(payload) = 'object')
);

CREATE INDEX IF NOT EXISTS idx_sync_pending
  ON sync_queue (status, next_attempt_at, source_node_id, event_sequence);

CREATE TABLE IF NOT EXISTS webhook_endpoints (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  secret_ref TEXT NOT NULL,
  events TEXT[] NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS webhook_deliveries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  endpoint_id UUID NOT NULL REFERENCES webhook_endpoints(id),
  alert_id UUID REFERENCES alerts(id),
  event_name TEXT NOT NULL,
  delivery_id TEXT NOT NULL UNIQUE,
  payload JSONB NOT NULL,
  signature TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'delivered', 'retrying', 'failed', 'dead_letter')),
  attempts SMALLINT NOT NULL DEFAULT 0 CHECK (attempts >= 0),
  next_attempt_at TIMESTAMPTZ,
  last_error TEXT,
  delivered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (jsonb_typeof(payload) = 'object')
);

CREATE INDEX IF NOT EXISTS idx_webhook_delivery_retry
  ON webhook_deliveries (status, next_attempt_at);

CREATE TABLE IF NOT EXISTS retention_policies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT NOT NULL UNIQUE,
  hot_days INTEGER CHECK (hot_days > 0),
  warm_days INTEGER CHECK (warm_days > 0),
  archive_days INTEGER CHECK (archive_days > 0),
  legal_hold_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  updated_by UUID REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS model_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL,
  event_captured_at TIMESTAMPTZ NOT NULL,
  label TEXT NOT NULL CHECK (label IN ('true_positive', 'false_positive')),
  reason TEXT NOT NULL,
  frame_ids TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  track_id TEXT,
  camera_id UUID NOT NULL REFERENCES cameras(id),
  model_id UUID REFERENCES models(id),
  rule_version INTEGER,
  anonymized_sample_uri TEXT,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (event_id, event_captured_at)
    REFERENCES event_index(id, captured_at) DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS idx_model_feedback_time
  ON model_feedback (model_id, created_at DESC);

CREATE MATERIALIZED VIEW IF NOT EXISTS events_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '1 hour', captured_at) AS bucket,
  site_id,
  category,
  severity,
  count(*) AS event_count
FROM events
GROUP BY bucket, site_id, category, severity
WITH NO DATA;

ALTER TABLE events SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'site_id,camera_id'
);
ALTER TABLE detections SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'camera_id,object_class'
);
ALTER TABLE health_metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id,metric_name'
);
ALTER TABLE camera_health SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'camera_id'
);
ALTER TABLE anpr_reads SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'site_id,camera_id'
);
ALTER TABLE face_matches SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'site_id,camera_id'
);

SELECT add_compression_policy('events', INTERVAL '7 days', if_not_exists => TRUE);
SELECT add_compression_policy('detections', INTERVAL '1 day', if_not_exists => TRUE);
SELECT add_compression_policy('health_metrics', INTERVAL '1 day', if_not_exists => TRUE);
SELECT add_compression_policy('camera_health', INTERVAL '1 day', if_not_exists => TRUE);
SELECT add_compression_policy('anpr_reads', INTERVAL '1 day', if_not_exists => TRUE);
SELECT add_compression_policy('face_matches', INTERVAL '1 day', if_not_exists => TRUE);

SELECT add_retention_policy('events', INTERVAL '365 days', if_not_exists => TRUE);
SELECT add_retention_policy('detections', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_retention_policy('health_metrics', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_retention_policy('camera_health', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_retention_policy('anpr_reads', INTERVAL '180 days', if_not_exists => TRUE);
SELECT add_retention_policy('face_matches', INTERVAL '180 days', if_not_exists => TRUE);

CREATE TRIGGER trg_organizations_updated_at
  BEFORE UPDATE ON organizations
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_sites_updated_at
  BEFORE UPDATE ON sites
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_devices_updated_at
  BEFORE UPDATE ON devices
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_cameras_updated_at
  BEFORE UPDATE ON cameras
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_alert_rules_updated_at
  BEFORE UPDATE ON alert_rules
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_alerts_updated_at
  BEFORE UPDATE ON alerts
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_sync_queue_updated_at
  BEFORE UPDATE ON sync_queue
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();
CREATE TRIGGER trg_webhook_endpoints_updated_at
  BEFORE UPDATE ON webhook_endpoints
  FOR EACH ROW EXECUTE FUNCTION falcon_set_updated_at();

CREATE TRIGGER trg_audit_logs_immutable
  BEFORE UPDATE OR DELETE ON audit_logs
  FOR EACH ROW EXECUTE FUNCTION falcon_reject_immutable_change();
CREATE TRIGGER trg_alert_actions_immutable
  BEFORE UPDATE OR DELETE ON alert_actions
  FOR EACH ROW EXECUTE FUNCTION falcon_reject_immutable_change();
CREATE TRIGGER trg_evidence_access_log_immutable
  BEFORE UPDATE OR DELETE ON evidence_access_log
  FOR EACH ROW EXECUTE FUNCTION falcon_reject_immutable_change();
CREATE TRIGGER trg_ledger_entries_immutable
  BEFORE UPDATE OR DELETE ON ledger_entries
  FOR EACH ROW EXECUTE FUNCTION falcon_reject_immutable_change();
CREATE TRIGGER trg_ledger_blocks_immutable
  BEFORE UPDATE OR DELETE ON ledger_blocks
  FOR EACH ROW EXECUTE FUNCTION falcon_reject_immutable_change();

-- Assign INSERT-only grants for audit_logs and ledger tables to the application
-- role in deployment migrations; table ownership remains with the migration role.
