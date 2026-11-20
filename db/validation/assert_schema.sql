DO $$
DECLARE
  required_hypertable RECORD;
  expected_policy RECORD;
  hypertable_names TEXT[] := ARRAY[
    'events',
    'detections',
    'anpr_reads',
    'face_matches',
    'health_metrics',
    'camera_health'
  ];
  hypertable_count INTEGER;
  compression_policy_count INTEGER;
  retention_policy_count INTEGER;
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_extension
    WHERE extname = 'timescaledb'
  ) THEN
    RAISE EXCEPTION 'TimescaleDB extension is not installed';
  END IF;

  FOR required_hypertable IN
    SELECT *
    FROM (VALUES
      ('events', 'captured_at'),
      ('detections', 'detected_at'),
      ('anpr_reads', 'read_at'),
      ('face_matches', 'matched_at'),
      ('health_metrics', 'sampled_at'),
      ('camera_health', 'sampled_at')
    ) AS expected(table_name, time_column)
  LOOP
    IF NOT EXISTS (
      SELECT 1
      FROM timescaledb_information.hypertables
      WHERE hypertable_name = required_hypertable.table_name
    ) THEN
      RAISE EXCEPTION 'Expected hypertable % is missing', required_hypertable.table_name;
    END IF;

    IF NOT EXISTS (
      SELECT 1
      FROM pg_constraint constraint_row
      WHERE constraint_row.conrelid =
        format('%I', required_hypertable.table_name)::REGCLASS
        AND constraint_row.contype = 'p'
        AND EXISTS (
          SELECT 1
          FROM unnest(constraint_row.conkey) AS key_column(attnum)
          JOIN pg_attribute attribute_row
            ON attribute_row.attrelid = constraint_row.conrelid
            AND attribute_row.attnum = key_column.attnum
          WHERE attribute_row.attname = required_hypertable.time_column
        )
    ) THEN
      RAISE EXCEPTION
        'Primary key for hypertable % must include partition column %',
        required_hypertable.table_name,
        required_hypertable.time_column;
    END IF;
  END LOOP;

  SELECT count(DISTINCT hypertable_name)
  INTO hypertable_count
  FROM timescaledb_information.jobs
  WHERE proc_name::TEXT LIKE '%policy_compression%'
    AND hypertable_name = ANY (hypertable_names);

  compression_policy_count := hypertable_count;
  IF compression_policy_count <> cardinality(hypertable_names) THEN
    RAISE EXCEPTION
      'Expected compression policies for % hypertables, found %',
      cardinality(hypertable_names),
      compression_policy_count;
  END IF;

  SELECT count(DISTINCT hypertable_name)
  INTO retention_policy_count
  FROM timescaledb_information.jobs
  WHERE proc_name::TEXT LIKE '%policy_retention%'
    AND hypertable_name = ANY (hypertable_names);

  IF retention_policy_count <> cardinality(hypertable_names) THEN
    RAISE EXCEPTION
      'Expected retention policies for % hypertables, found %',
      cardinality(hypertable_names),
      retention_policy_count;
  END IF;

  FOR expected_policy IN
    SELECT *
    FROM (VALUES
      ('events', 'policy_compression', 'compress_after', '7 days'),
      ('detections', 'policy_compression', 'compress_after', '1 day'),
      ('anpr_reads', 'policy_compression', 'compress_after', '1 day'),
      ('face_matches', 'policy_compression', 'compress_after', '1 day'),
      ('health_metrics', 'policy_compression', 'compress_after', '1 day'),
      ('camera_health', 'policy_compression', 'compress_after', '1 day'),
      ('events', 'policy_retention', 'drop_after', '365 days'),
      ('detections', 'policy_retention', 'drop_after', '30 days'),
      ('anpr_reads', 'policy_retention', 'drop_after', '180 days'),
      ('face_matches', 'policy_retention', 'drop_after', '180 days'),
      ('health_metrics', 'policy_retention', 'drop_after', '30 days'),
      ('camera_health', 'policy_retention', 'drop_after', '30 days')
    ) AS expected(hypertable_name, procedure_name, config_key, interval_value)
  LOOP
    IF NOT EXISTS (
      SELECT 1
      FROM timescaledb_information.jobs job
      WHERE job.hypertable_name = expected_policy.hypertable_name
        AND job.proc_name::TEXT LIKE '%' || expected_policy.procedure_name || '%'
        AND (job.config ->> expected_policy.config_key)::INTERVAL =
          expected_policy.interval_value::INTERVAL
    ) THEN
      RAISE EXCEPTION
        'Expected % policy on % with interval %',
        expected_policy.procedure_name,
        expected_policy.hypertable_name,
        expected_policy.interval_value;
    END IF;
  END LOOP;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE contype = 'f'
      AND conrelid = 'alerts'::REGCLASS
      AND confrelid = 'event_index'::REGCLASS
  ) THEN
    RAISE EXCEPTION 'Expected alert-to-event identity foreign key is missing';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_indexes
    WHERE schemaname = current_schema()
      AND indexname = 'idx_alert_status_severity_time'
  ) THEN
    RAISE EXCEPTION 'Expected alert status/severity index is missing';
  END IF;
END;
$$;

SELECT hypertable_name, proc_name, config
FROM timescaledb_information.jobs
WHERE proc_name::TEXT LIKE '%policy_compression%'
   OR proc_name::TEXT LIKE '%policy_retention%'
ORDER BY hypertable_name, proc_name;
