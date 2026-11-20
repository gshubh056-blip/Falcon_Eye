# Database migrations

The initial migration applies the immutable `baseline.sql` snapshot copied
from `db/schema.sql`. Keep that snapshot and revision unchanged; schema changes
after this baseline belong in new ordered Alembic revisions.

Set `DATABASE_URL` to a PostgreSQL/TimescaleDB database using the `psycopg`
SQLAlchemy driver, then run from the repository root:

```powershell
uv run alembic -c db/alembic.ini upgrade head
uv run python scripts/seed_data.py
```

The seed creates only synthetic local organization, site, device, disabled
camera, and operator records. It creates no password or camera stream
credentials. Run `db\validation\validate_migrations.ps1` to exercise upgrade,
downgrade, re-upgrade, and repeated seeding on a disposable database.