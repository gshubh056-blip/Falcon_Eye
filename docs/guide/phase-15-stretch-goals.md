# Phase 15 - Stretch Goals

## STEP 15.1 – [P2] Cross-camera re-ID
- **Goal:** Appearance embeddings associate observations across overlapping cameras.
- **Implements:** FR-016.
- **Owner / Time:** CV/ML; 180 minutes.
- **Prerequisites:** M2 and controlled overlapping data.
- **Why this step:** Re-ID can improve coordination but is not a P0 safety feature.
- **Do this (micro-steps):**
  1. Extract appearance embedding.
  2. Match across camera candidates.
  3. Require confidence and human confirmation.
- **Expected result:** Re-ID returns candidate IDs only.
- **Verify:** `pytest tests/system/test_cross_camera_reid.py -q`.
- **If it fails:** No overlap: leave disabled.
- **Git commit:** `git add apps/tracker && git commit -m "feat: add optional cross-camera re-ID"`
- **Done when:** Stretch target is benchmarked and candidate-only.

## STEP 15.2 – [P2] Drone/UAV detection head
- **Goal:** A drone class is added without changing core architecture.
- **Implements:** FR-057.
- **Owner / Time:** CV/ML; 120 minutes.
- **Prerequisites:** Licensed aerial dataset.
- **Why this step:** A modular head proves extensibility.
- **Do this (micro-steps):**
  1. Add drone/UAV class to a separate head.
  2. Produce track/alert JSON using existing alert engine.
- **Expected result:** A UAV frame produces a candidate alert.
- **Verify:** `python scripts/evaluate_model.py --task drone`.
- **If it fails:** False positives high: keep disabled.
- **Git commit:** `git add apps/inference_service && git commit -m "feat: add optional UAV detection head"`
- **Done when:** Model and license report pass.

## STEP 15.3 – [P2] Fabric Merkle anchoring
- **Goal:** Signed roots anchor to a permissioned Fabric test network.
- **Implements:** P2 ledger.
- **Owner / Time:** Security/DevOps; 240 minutes.
- **Prerequisites:** P1 Merkle and Docker resources.
- **Why this step:** Fabric demonstrates the theme without making it mandatory for MVP.
- **Do this (micro-steps):**
  1. Deploy one peer, orderer and CA for test only.
  2. Add chaincode that stores Merkle root, node and timestamp.
  3. Never store raw video or face embeddings.
- **Expected result:** A signed root is visible in ledger transaction.
- **Verify:** `pytest tests/integration/test_fabric_anchor.py -q`.
- **If it fails:** Resource limit: keep local anchor and mark Fabric stretch.
- **Git commit:** `git add deploy/fabric apps/ledger_service && git commit -m "feat: add optional Fabric anchor adapter"`
- **Done when:** P2 test network anchors one root.

## STEP 15.4 – [P2] Add multilingual UI and cloud hybrid
- **Goal:** Hindi and optional HQ cloud remain adapters.
- **Implements:** NFR-010.
- **Owner / Time:** Frontend/DevOps; 150 minutes.
- **Prerequisites:** MVP stable.
- **Why this step:** It localizes only after core operator workflow is complete.
- **Do this (micro-steps):**
  1. Add i18n English/Hindi resources.
  2. Keep all IDs and severity names language-independent.
  3. Add cloud adapter behind edge sync interface.
- **Expected result:** Language switch changes visible labels and cloud sync remains optional.
- **Verify:** `npm run test && pytest tests/integration/test_sync.py -q`.
- **If it fails:** Translation missing: English fallback remains.
- **Git commit:** `git add apps/dashboard apps/sync_service && git commit -m "feat: add optional Hindi and cloud adapters"`
- **Done when:** MVP behavior does not depend on stretch adapters.

## Phase checklist
- [ ] Re-ID remains candidate-only.
- [ ] UAV is licensed and measurable.
- [ ] Fabric stores only roots.
- [ ] Hindi/cloud are optional.

## Phase demo
Show one stretch feature only if it has passed model and security gates.

## Rollback
Disable feature flags and keep P0/P1 services.

## Time summary
Phase 15 takes approximately 690 minutes.
