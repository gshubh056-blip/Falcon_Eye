# Phase 12 - Security Hardening

## STEP 12.1 – [P0 MVP] Create an internal CA and mTLS
- **Goal:** Edge and service calls authenticate with certificates.
- **Implements:** SEC-001.
- **Owner / Time:** Security/DevOps; 90 minutes.
- **Prerequisites:** Docker network and service identities.
- **Why this step:** Password-free mutual service authentication reduces spoofed nodes.
- **Do this (micro-steps):**
  1. Use an internal CA script.
  2. Generate one server and one client certificate per service.
  3. Mount certificates read-only.
- **Expected result:** Plain HTTP cross-service call fails.
- **Verify:** `pytest tests/security/test_mtls.py -q`.
- **If it fails:** SAN mismatch: regenerate certificate with exact service DNS name.
- **Git commit:** `git add deploy/certs scripts tests/security && git commit -m "security: add local mTLS certificates"`
- **Done when:** Service-to-service mTLS test passes.

## STEP 12.2 – [P0 MVP] Move secrets to environment/key store
- **Goal:** RTSP credentials and signing keys never appear in Git.
- **Implements:** SEC-004.
- **Owner / Time:** Security; 45 minutes.
- **Prerequisites:** `.env.example`.
- **Why this step:** Secret rotation and review require references outside source.
- **Do this (micro-steps):**
  1. Create `.env.example` only.
  2. Add `.env`, `*.pem`, `*.key` to `.gitignore`.
  3. Store RTSP credentials by `credential_ref`.
- **Expected result:** Git secret scan finds no secret.
- **Verify:** `git grep -n "PASSWORD\\|PRIVATE KEY" -- ':!docs/PRD.md'`.
- **If it fails:** Secret in history: rotate it and purge through approved repository process.
- **Git commit:** `git add .gitignore .env.example && git commit -m "security: protect local secrets"`
- **Done when:** Git and API export contain no raw credentials.

## STEP 12.3 – [P0 MVP] Verify RBAC and MFA
- **Goal:** Privileged actions require role and MFA.
- **Implements:** SEC-002, SEC-003.
- **Owner / Time:** Security/Backend; 75 minutes.
- **Prerequisites:** Phase 5 auth.
- **Why this step:** Unauthorized alert, watchlist or model actions are security incidents.
- **Do this (micro-steps):**
  1. Implement matrix negative tests.
  2. Require MFA for admin/model/user actions.
  3. Audit every denied action.
- **Expected result:** Negative tests return 403 and add audit row.
- **Verify:** `pytest tests/security/test_rbac.py tests/security/test_mfa.py -q`.
- **If it fails:** 200 instead of 403: endpoint lacks role dependency.
- **Git commit:** `git add tests/security apps/api_gateway && git commit -m "security: enforce RBAC and MFA"`
- **Done when:** All matrix cases pass.

## STEP 12.4 – [P0 MVP] Encrypt evidence and storage
- **Goal:** Disk and object evidence use encrypted storage.
- **Implements:** SEC, FR-083.
- **Owner / Time:** Security/DevOps; 60 minutes.
- **Prerequisites:** MinIO and edge disk.
- **Why this step:** Stolen disks or objects must not expose video.
- **Do this (micro-steps):**
  1. Enable MinIO encryption or signed S3 key.
  2. Document BitLocker/LUKS/OS disk encryption.
  3. Expire signed links after 15 minutes.
- **Expected result:** Signed link expires and object is unreadable without key.
- **Verify:** `pytest tests/security/test_signed_links.py -q`.
- **If it fails:** Link remains valid: enforce epoch and expiration in signature.
- **Git commit:** `git add deploy apps/event_service && git commit -m "security: add evidence encryption and signed links"`
- **Done when:** Encryption and expiry tests pass.

## STEP 12.5 – [P0 MVP] Scan dependencies, images and SBOM
- **Goal:** Critical/high dependency findings are visible and triaged.
- **Implements:** SEC-005.
- **Owner / Time:** Security/DevOps; 90 minutes.
- **Prerequisites:** Docker and CI.
- **Why this step:** Untrusted dependencies can compromise the edge.
- **Do this (micro-steps):**
  1. Generate Python SBOM using an approved tool.
  2. Run `pip-audit`.
  3. Run Trivy image scan.
  4. Block critical/high without approved exception.
- **Expected result:** SBOM and scan reports exist in CI artifacts.
- **Verify:** `pip-audit -r requirements.txt`, `trivy image falcon/api:local`.
- **If it fails:** Tool unavailable: pin/install in CI. Finding unfixable: document exception/owner/expiry.
- **Git commit:** `git add .github/workflows reports && git commit -m "security: add SBOM and dependency scanning"`
- **Done when:** No unapproved critical/high finding remains.

## Phase checklist
- [ ] mTLS passes.
- [ ] Secrets are not in Git.
- [ ] RBAC/MFA pass.
- [ ] Evidence encryption and link expiry pass.
- [ ] SBOM/image scans pass.

## Phase demo
Show denied role, encrypted evidence, signed ledger and SBOM for the final image.

## Rollback
Restore demo HTTP local-only profile only on an isolated laptop; never expose this rollback to field network.

## Time summary
Phase 12 takes approximately 360 minutes.
