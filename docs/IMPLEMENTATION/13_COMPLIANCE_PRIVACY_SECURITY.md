# Compliance, Privacy and Security Plan

This is an engineering checklist and threat-review scaffold, not legal advice, certification, or proof of compliance. A qualified privacy/security/legal reviewer and deployment authority must approve the jurisdiction-specific requirements before any operational camera or biometric data is processed.

## Data classes and controls

| Data class | Examples | Required controls |
|---|---|---|
| Credentials/secrets | RTSP password, ONVIF credentials, API tokens, signing keys | Secret references only; encryption at rest; scoped access; rotation; never logged/exported; redact URLs |
| Video/evidence | Frame, snapshot, clip, audio if any | Explicit source authorization; encrypted storage; signed short-lived link; access log; retention/legal hold; export approval |
| Detection metadata | Bbox, track ID, timestamps, camera/site, rule explanation | Site-scoped access; purpose-bound search; minimal retention; protect location/security context |
| Face/biometric | Face crop, embedding, watchlist identity, match score | Disabled by default; documented legal basis/purpose/notice; consent or lawful authorization; strict role/purpose; expiry; encryption; quality threshold; human review; deletion propagation |
| Plate/vehicle | Plate text, crop, location/time, watchlist match | Purpose-limited search, access logging, retention limits, human confirmation and false-match handling |
| Audit/ledger | Actor, purpose, resource, action, hash/signature | Append-only service account; immutable storage/backup; restricted read; chain validation and time synchronization |
| Model/dataset | Weights, training clips, labels, embeddings | License/provenance/SBOM, signatures, checksum, access review, export controls, privacy review |

## Privacy-by-design checklist

- [ ] Document deployment purpose, controller/operator responsibilities, lawful basis, notices, rights/retention and complaint path with competent reviewers.
- [ ] Do not assume the national-security context removes privacy or data-protection obligations.
- [ ] Minimize collection: process only configured classes/ROIs; do not save continuous video by default where PRD permits event-only evidence.
- [ ] Separate synthetic demo identities from any real watchlist; test/demo defaults have no real faces or plates.
- [ ] Gate FRS behind explicit deployment approval and a feature flag off by default.
- [ ] Record who searched/enrolled/exported face or plate data, purpose, case/reference, time, threshold, candidate and human decision.
- [ ] Use quality thresholds and present identity matches as candidates only; no match is the sole basis for enforcement.
- [ ] Apply configurable retention, legal hold and deletion across DB, object store, replicas, caches, vector indexes and sync nodes.
- [ ] Provide deletion/hold verification and audit evidence; never erase an active legal hold automatically.
- [ ] Obtain authorization for all footage, test scenes, public datasets, annotations, logos/fonts and pretrained models.
- [ ] Redact sensitive details from logs, traces, crash dumps, bug reports and support packages.
- [ ] Review maps/tiles: no unapproved external basemap requests or coordinate disclosures from an air-gapped site.

## Security implementation checklist

### Identity and authorization

- [ ] Argon2id password hashing with parameters documented and migrated safely.
- [ ] Short-lived JWT/access tokens and rotating refresh credentials; TRD access token target 15 minutes.
- [ ] MFA required for privileged roles; recovery flow tested and audited.
- [ ] Deny by default; enforce PRD role and site scope at API/service/repository boundaries.
- [ ] Service accounts are distinct from human roles; API keys hashed, scoped, rotated and revocable.
- [ ] Rate limits and lockout controls are observable and do not disclose account existence.

### Network, API and camera input

- [ ] TLS 1.2+ externally and mTLS for edge service traffic per PRD.
- [ ] CORS allowlist, security headers, request size/time limits, schema validation and correlation IDs.
- [ ] SSRF controls on RTSP/ONVIF/webhook addresses: validate schemes, resolve/deny loopback/link-local/metadata addresses as policy requires, restrict egress, revalidate redirects/DNS.
- [ ] Camera credentials stored as encrypted secret references; raw passwords never returned or logged.
- [ ] Use ONVIF/RTSP test network isolation; PTZ/siren actions require explicit permissions and auditable safeguards.
- [ ] Webhook HMAC covers canonical request bytes and timestamp/nonce; retry/replay policy is bounded; endpoint verification prevents internal-network abuse.
- [ ] Validate file upload type, size, path and archive expansion; store outside executable/static paths.

### Evidence, ledger and data at rest

- [ ] AES-256 envelope encryption for evidence; key references and rotation process; secure deletion policy.
- [ ] SHA-256 content and metadata hashes; exact previous entry hash; Ed25519 signatures; Merkle batch verification.
- [ ] `/api/v1/evidence/{event_id}/verify` returns distinct valid/tampered/incomplete/unavailable outcomes with evidence chain details.
- [ ] External chain anchor is optional and cannot block local verification; never call a local hash chain a decentralized blockchain.
- [ ] Hash/signature prove integrity since capture under the key assumptions, not that the original scene or model interpretation is true.
- [ ] Audit logs are append-only for application role; access/export attempts are logged; chain and backup tested.
- [ ] Signed evidence links expire within 15 minutes and recheck authorization at fetch time.

### Supply chain and operations

- [ ] Pin dependencies, containers, model/runtime, dataset manifests and licenses; generate SBOM.
- [ ] Verify image/model signatures and hashes before startup/promotion; maintain rollback artifact.
- [ ] Separate build, signing and deployment privileges; protect signing keys in secret storage.
- [ ] Scan dependencies, containers, code and secrets; triage vulnerabilities with owner and due date.
- [ ] Structured logs avoid PII; include request/event/camera/node IDs as PRD requires.
- [ ] Backup DB/object metadata/keys according to an approved recovery plan; test restore and key recovery.
- [ ] Watch disk thresholds (10% warning, 5% safe mode), queue depth, service restarts and camera status.
- [ ] Incident response covers lost device, credential compromise, evidence tamper, model compromise, unauthorized data access and sync conflict.

## STRIDE summary

| STRIDE class | FALCON examples | Minimum mitigation / verification |
|---|---|---|
| Spoofing | Forged camera node, stolen JWT, fake model publisher | mTLS/device identity, MFA, signatures; invalid identity tests |
| Tampering | Altered frame/evidence/model/zone config or sync payload | Hash/signature, versioned config, authorization, idempotency; tamper tests |
| Repudiation | Operator denies alert action or evidence export | Append-only audit with actor, purpose, request ID, chain verification |
| Information disclosure | Camera secrets in URL/log, cross-site evidence or face data leak | Secret refs/redaction, encryption, RBAC/site scopes, signed links, access tests |
| Denial of service | RTSP exhaustion, huge polygon/upload, queue/broker overload | Bounded queues, timeouts, input limits, rate limits, backpressure, watchdog |
| Elevation of privilege | Weak role check, compromised worker, unsafe PTZ/siren | Server-side least privilege, service identities, dual control where required, negative RBAC tests |

## Human factors and responsible AI

- Alerts are cues for trained operators, not determinations of guilt or autonomous enforcement.
- Display source camera/time, confidence, rule threshold, track/zone and evidence availability; do not hide uncertainty.
- Measure false positives and false negatives by class/scene/lighting; report insufficient data instead of asserting fairness.
- Face recognition threshold must derive from a governed validation set and FAR/FRR target, be versioned and reviewable.
- Avoid alert language that implies a person is criminal based on watchlist or behavior prediction.
- Operators can mark false positives with a reason; feedback is audited and reviewed before training use.
- Training and interface design should not incentivize alert-count targets or unsafe response escalation.

## Approval gates

No live data or field deployment before: (1) named system/data owner, (2) legal/privacy assessment, (3) threat model and security review, (4) camera/site authorization, (5) retention and access policy, (6) tested backup/incident response, and (7) trained operators and fallback. Record reviewer, date, scope, conditions and open findings in the project release evidence.

