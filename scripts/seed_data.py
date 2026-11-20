import os

from sqlalchemy import create_engine, text


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required to seed local synthetic data.")

    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.begin() as connection:
            organization_id = connection.execute(
                text(
                    """
                    INSERT INTO organizations (name, code)
                    VALUES (:name, :code)
                    ON CONFLICT (code) DO UPDATE
                    SET name = EXCLUDED.name, active = TRUE
                    RETURNING id
                    """
                ),
                {"name": "Synthetic Demo Organization", "code": "synthetic-demo"},
            ).scalar_one()

            site_id = connection.execute(
                text(
                    """
                    INSERT INTO sites (organization_id, name, code, site_type)
                    VALUES (:organization_id, :name, :code, 'demo')
                    ON CONFLICT (code) DO UPDATE
                    SET organization_id = EXCLUDED.organization_id,
                        name = EXCLUDED.name,
                        site_type = EXCLUDED.site_type
                    RETURNING id
                    """
                ),
                {
                    "organization_id": organization_id,
                    "name": "Synthetic Demo Site",
                    "code": "synthetic-demo-site",
                },
            ).scalar_one()

            device_id = connection.execute(
                text(
                    """
                    INSERT INTO devices (
                      site_id, hostname, hardware_profile, software_version, status
                    )
                    VALUES (
                      :site_id, 'synthetic-edge-01', 'synthetic', 'demo', 'maintenance'
                    )
                    ON CONFLICT (site_id, hostname) DO UPDATE
                    SET hardware_profile = EXCLUDED.hardware_profile,
                        software_version = EXCLUDED.software_version,
                        status = EXCLUDED.status
                    RETURNING id
                    """
                ),
                {"site_id": site_id},
            ).scalar_one()
            connection.execute(
                text("UPDATE sites SET edge_node_id = :device_id WHERE id = :site_id"),
                {"device_id": device_id, "site_id": site_id},
            )

            connection.execute(
                text(
                    """
                    INSERT INTO cameras (
                      site_id, device_id, name, protocol, camera_type, status, enabled, config
                    )
                    VALUES (
                      :site_id, :device_id, 'Synthetic File Camera', 'file',
                      'visible', 'disabled', FALSE, '{"synthetic": true}'::jsonb
                    )
                    ON CONFLICT (site_id, name) DO UPDATE
                    SET device_id = EXCLUDED.device_id,
                        protocol = EXCLUDED.protocol,
                        stream_uri = NULL,
                        credential_ref = NULL,
                        camera_type = EXCLUDED.camera_type,
                        status = 'disabled',
                        enabled = FALSE,
                        config = EXCLUDED.config
                    """
                ),
                {"site_id": site_id, "device_id": device_id},
            )

            user_id = connection.execute(
                text(
                    """
                    INSERT INTO users (subject, display_name, email, mfa_required)
                    VALUES (
                      'synthetic:falcon-demo-operator',
                      'Synthetic Demo Operator',
                      'demo.operator@example.invalid',
                      TRUE
                    )
                    ON CONFLICT (subject) DO UPDATE
                    SET display_name = EXCLUDED.display_name,
                        email = EXCLUDED.email,
                        mfa_required = TRUE,
                        active = TRUE
                    RETURNING id
                    """
                )
            ).scalar_one()

            role_id = connection.execute(
                text("SELECT id FROM roles WHERE name = 'operator'")
            ).scalar_one()
            connection.execute(
                text(
                    """
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (:user_id, :role_id)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                    """
                ),
                {"user_id": user_id, "role_id": role_id},
            )
            connection.execute(
                text(
                    """
                    INSERT INTO user_site_access (user_id, site_id)
                    VALUES (:user_id, :site_id)
                    ON CONFLICT (user_id, site_id) DO NOTHING
                    """
                ),
                {"user_id": user_id, "site_id": site_id},
            )
    finally:
        engine.dispose()

    print("Synthetic local seed is ready; camera remains disabled.")


if __name__ == "__main__":
    main()
