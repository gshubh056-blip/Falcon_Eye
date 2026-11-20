from pathlib import Path

from alembic import op

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    schema_path = Path(__file__).resolve().parents[1] / "baseline.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    # Psycopg interprets percent markers as placeholders even without bound values.
    op.get_bind().exec_driver_sql(schema_sql.replace("%", "%%"))


def downgrade() -> None:
    connection = op.get_bind()
    connection.exec_driver_sql("DROP MATERIALIZED VIEW IF EXISTS events_hourly")
    for table_name in (
        "model_feedback",
        "retention_policies",
        "webhook_deliveries",
        "webhook_endpoints",
        "sync_queue",
        "camera_health",
        "health_metrics",
        "audit_logs",
        "ledger_blocks",
        "ledger_entries",
        "evidence_access_log",
        "evidence_files",
        "face_matches",
        "face_embeddings",
        "watchlist_faces",
        "anpr_reads",
        "watchlist_plates",
        "alert_deliveries",
        "alert_actions",
        "alerts",
        "detections",
        "events",
        "event_index",
        "tracks",
        "alert_rules",
        "configs",
        "camera_model_assignments",
        "models",
        "zones",
        "api_keys",
        "auth_sessions",
        "user_site_access",
        "user_roles",
        "roles",
        "users",
        "cameras",
        "devices",
        "sites",
        "organizations",
    ):
        connection.exec_driver_sql(f"DROP TABLE IF EXISTS {table_name} CASCADE")
    connection.exec_driver_sql("DROP FUNCTION IF EXISTS falcon_set_updated_at() CASCADE")
    connection.exec_driver_sql("DROP FUNCTION IF EXISTS falcon_reject_immutable_change() CASCADE")
    for enum_name in (
        "falcon_evidence_kind",
        "falcon_zone_direction",
        "falcon_zone_type",
        "falcon_camera_type",
        "falcon_alert_status",
        "falcon_severity",
    ):
        connection.exec_driver_sql(f"DROP TYPE IF EXISTS {enum_name}")
