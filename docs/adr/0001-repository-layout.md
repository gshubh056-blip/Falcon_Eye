# ADR-0001: Repository Layout

- Status: Accepted
- Date: 2026-11-19
- Context: The TRD is the technical authority for package layout and service boundaries.
- Decision: Keep the implementation in `apps/`, `pipeline/`, `db/`, `deploy/`, `tests/`,
  `docs/`, and `scripts/`. Do not create a parallel `web/` or `frontend/` tree.
- Consequences: The React application remains in `apps/dashboard/`. Python services
  remain under `apps/`. Shared contracts must live outside service-specific folders.
- Evidence: [TRD](/C:/Users/rg849/OneDrive/Pictures/OneDrive/Desktop/Falcon_Eye/docs/TRD.md)
  Section 3.
