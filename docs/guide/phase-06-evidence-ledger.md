# Phase 06 - Evidence Integrity Ledger

## STEP 6.1 – [P0 MVP] Generate canonical JSON
- **Goal:** Identical evidence metadata produces one identical SHA-256 value.
- **Implements:** SEC-006, DB-002.
- **Owner / Time:** Security/Backend; 45 minutes.
- **Prerequisites:** Evidence records from Phase 4.
- **Why this step:** Canonicalization prevents formatting differences from changing the hash.
- **Do this (micro-steps):**
  1. Create `apps/ledger_service/canonical.py`.
  2. Sort keys, emit UTF-8 JSON and exclude volatile fields.
  3. Test key order.
- **Expected result:** Two differently ordered dictionaries produce the same hash.
- **Verify:** `pytest tests/unit/test_canonical.py -q`.
- **If it fails:** NaN or datetime present: convert only to ISO UTC strings.
- **Git commit:** `git add apps/ledger_service/canonical.py && git commit -m "feat: add canonical evidence JSON"`
- **Done when:** Canonical hash test passes.

## STEP 6.2 – [P0 MVP] Generate and secure Ed25519 keys
- **Goal:** The edge node owns a non-public signing key.
- **Implements:** SEC-004, SEC-005.
- **Owner / Time:** Security; 30 minutes.
- **Prerequisites:** Python cryptography package.
- **Why this step:** Ed25519 proves which node signed the evidence record.
- **Do this (micro-steps):**
  1. Generate private/public key with cryptography.
  2. Store private key outside Git under `keys/edge-private.pem`.
  3. Add `keys/` to `.gitignore`.
- **Expected result:** Private key mode is owner-only and public key exists.
- **Verify:** `openssl pkey -in keys/edge-private.pem -pubout -out keys/edge-public.pem`.
- **If it fails:** Private key found in Git: remove and rotate it; never paste into chat.
- **Git commit:** `git add .gitignore apps/ledger_service && git commit -m "security: add local Ed25519 signing support"`
- **Done when:** Signing key is untracked and public key validates signatures.

## STEP 6.3 – [P0 MVP] Append hash-chained ledger entries
- **Goal:** Every evidence entry stores previous hash and Ed25519 signature.
- **Implements:** SEC-006, DB-002.
- **Owner / Time:** Security/Backend; 90 minutes.
- **Prerequisites:** Steps 6.1–6.2.
- **Why this step:** Chain append detects deletion and content modification.
- **Do this (micro-steps):**
  1. Lock with a database transaction.
  2. Read the latest `entry_hash`.
  3. Set `prev_hash`, evidence hash and metadata hash.
  4. Sign `entry_hash` with Ed25519.
- **Expected result:** Every second entry references the first entry hash.
- **Verify:** `pytest tests/integration/test_ledger.py -q`.
- **If it fails:** Lock conflict: retry once, then queue. Chain mismatch: do not overwrite; quarantine node.
- **Git commit:** `git add apps/ledger_service tests/integration/test_ledger.py && git commit -m "feat: append signed hash-chain ledger entries"`
- **Done when:** Chain and signature tests pass.

## STEP 6.4 – [P0 MVP] Verify evidence through CLI and API
- **Goal:** A modified clip or broken chain produces `invalid`.
- **Implements:** NFR-016, API-021.
- **Owner / Time:** Security; 60 minutes.
- **Prerequisites:** Step 6.3.
- **Why this step:** Verification is needed by operators and auditors.
- **Do this (micro-steps):**
  1. Create `scripts/verify_evidence.py`.
  2. Calculate evidence SHA-256.
  3. Verify Ed25519 signature and `prev_hash`.
  4. Add `/api/v1/evidence/{event_id}/verify`.
- **Expected result:** Original returns verified; one-byte modification returns tampered.
- **Verify:** `python scripts/verify_evidence.py --event-id <uuid> --object-file evidence/<event_id>/clip.mp4`.
- **If it fails:** Public key missing: add public key to verifier config. Signature mismatch: regenerate entry metadata canonically.
- **Git commit:** `git add scripts/verify_evidence.py apps/ledger_service apps/api_gateway && git commit -m "feat: add evidence CLI and verification API"`
- **Done when:** M3 and tamper demo pass.

## STEP 6.5 – [P1] Add Merkle batch anchoring
- **Goal:** Every 6-hour batch or 1000 entries receives a signed Merkle root.
- **Implements:** P1 ledger requirement.
- **Owner / Time:** Security; 60 minutes.
- **Prerequisites:** P0 ledger pass.
- **Why this step:** External batches provide efficient store-and-forward verification.
- **Do this (micro-steps):**
  1. Implement Merkle root from entry hashes.
  2. Sign root and store `merkle_root`, `anchor_status=pending`.
  3. Use local anchor backend file first.
- **Expected result:** Root verifies all batch entries.
- **Verify:** `pytest tests/unit/test_merkle.py tests/integration/test_anchor.py -q`.
- **If it fails:** Odd leaf count: duplicate final hash. Pending root: retain pending and retry.
- **Git commit:** `git add apps/ledger_service && git commit -m "feat: add local Merkle anchor backend"`
- **Done when:** Pending and verified anchor states are tested.

## Phase checklist
- [ ] Canonical JSON hash passes.
- [ ] Key generation is secure.
- [ ] P0 ledger chain verifies.
- [ ] Tamper API fails correctly.
- [ ] M3 and P1 Merkle pass.

## Phase demo
Show verified badge, modify one byte in a copy of the clip, and show tamper/fail status.

## Rollback
Disable anchoring, keep P0 ledger, and restore the previous public key from the approved key store.

## Time summary
Phase 6 takes approximately 285 minutes.
