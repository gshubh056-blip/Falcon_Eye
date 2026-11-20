# F1-01 PostgreSQL/TimescaleDB Validation

Docker Desktop (or a compatible Docker runtime) is required. The schema must
not be called validated based on static inspection alone; the successful
disposable run is recorded below.

Run from the repository root in PowerShell:

```powershell
.\db\validation\validate_schema.ps1
```

The script starts only the `postgres-validation` Compose profile, which uses
the pinned PostgreSQL 16/TimescaleDB image, a temporary filesystem data
directory, and host port 55432. It applies `db\schema.sql`, checks the six
hypertables, compression/retention policies, alert-to-event foreign key, and
alert index, then removes the disposable validation container. It does not
touch the persistent `postgres` service or its volume.

## Validation result

- Date: 2026-11-19
- Result: passed on a clean disposable PostgreSQL 16/TimescaleDB container.
- Image: `timescale/timescaledb:2.17.2-pg16@sha256:4e459e217f00cbb09920c34d245501e63427e6767a495de57ce76823ff280f12`
- Verified: six hypertables and time-partition primary keys; alert-to-event
  foreign key; alert status/severity index; six compression policies and six
  retention policies with the configured intervals.
- The validation container and its temporary data directory were removed.
- This does not verify retention deletion over time, application-role
  permissions, or production workload behavior.

## F1-02 migration and seed validation

Run from the repository root in PowerShell:

```powershell
.\db\validation\validate_migrations.ps1
```

This uses the disposable TimescaleDB service to verify an empty-database
Alembic upgrade, downgrade to base, re-upgrade, and two consecutive seed runs.
It asserts that the synthetic organization/site/operator and disabled camera
remain unique. The container uses a temporary filesystem and is removed when
the script exits.
