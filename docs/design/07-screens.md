# 07 — Screen Designs

This document covers every screen in `WEB_FLOW.md` and the additional screens requested by the UI/UX master prompt. Route and API identifiers follow `WEB_FLOW.md`; any action without backend support remains blocked/read-only.

## Shared shell

```text
+--------------------------------------------------------------------------+
| FALCON | Site + local clock | Node/WS status | Severity counts | User    |
+----------+---------------------------------------------------------------+
| Side nav | Global banner                                              |
|          +---------------------------------------------------------------+
|          | Breadcrumb / Page title / primary task                        |
|          | Main content                                          Details  |
+----------+---------------------------------------------------------------+
| Local API / HQ sync / storage status                                    |
+--------------------------------------------------------------------------+
```

The eye sees current connection and critical state first, page task second, supporting metadata third. All routes have loading skeleton, empty, error, offline/stale, permission-denied and partial-data states as defined in WEB_FLOW STA-15–20. No page may imply a successful mutation before server confirmation.

## Authentication and core operations

### SCR-01 Login / MFA

Desktop: 42% left brand panel with contour/radar art and wordmark; 58% right focused form card on Obsidian. At 2560 wall size, form remains centered and does not scale beyond readable width. Fields: username, password, MFA when challenged, language; primary Sign in. Hero is static for reduced motion; no external image/font. Loading disables duplicate submit; error is generic; offline explains authentication unavailable; locked status comes only from server. Signature moment: one subtle cyan sweep resolves to the angular mark. Setup wizard is unavailable until API-setup gap is closed.

### SCR-02 Operations Overview

Desktop: top strip has severity KPIs and node state; center is live alert queue (largest); right rail shows camera availability and health; map snapshot is secondary P1. Wall: critical/high alert summary and site health enlarge; no small paragraphs. Empty: “All clear” illustration and camera status. Partial data labels each widget with last update. Signature moment: calm summary turns to a stable, legible alert highlight, never an animated dashboard takeover.

### SCR-03 Live Wall (1/4/9/16)

Grid has 1, 2×2, 3×3 and 4×4 layouts; toolbar controls density, selection and overlay. Each tile has solid video plane, camera/time/status strip, optional corner-bracket overlay and optional zone outline. 1-view shows selected camera metadata/actions in side panel; 4/9/16 tiles use compact headers. Alert state adds severity border and label but never an uncontrolled flashing glow. Loading uses neutral skeleton; offline uses dashed border and last frame; unavailable stream has retry if supported. Low bandwidth explicitly defers clips. Signature moment: overlays stay registered to the frame; no live-video blur. Capacity is measured, not implied by grid option.

### SCR-04 Cameras admin / list

Table: camera name, group/site, protocol, connection, last frame, analytics state and permitted actions. Compact rows retain status text. Add-camera wizard: ONVIF discovery → manual RTSP → credential entry → test → preview → site/location if contract exists → save → analytics/zones only if supported. Credential never appears after save. Failure retains only safe form fields and a classified message.

### SCR-05 Camera Detail

Large player at left, camera identity/health panel at right, tabs for recent events, zones and health history. PTZ pad only for supported cameras and role. Show active analytics/model state only when backend provides it. Offline and degraded states show last frame and reconnect status. No video playback URL means show a safe unavailable player state rather than a raw RTSP URL.

### SCR-06 Alert Inbox

Desktop split view: filter rail (severity/type/site/camera/time/status/assignee) at 25%, result list at 35%, detail preview at 40%. At laptop/mobile, detail becomes drawer/page. Stable row anatomy: severity icon+label, title, camera, time, state, assignee/evidence as available. New alert pill appears above list; list does not jump while selected or scrolled. Empty filters show reset action. Signature moment: severity and state are understood before reading explanatory text.

### SCR-07 Alert / Incident Detail

Header: severity, title, state, timestamp, camera. Primary actions are acknowledge/review/escalate/resolve as role permits; false-positive action is separated and asks for reason. Body: XAI explanation, evidence preview, detection metadata, related events/map only when supplied, action timeline. Integrity seal appears only in evidence context. 409 shows refreshed state and action conflict. Signature moment: one concise explanation answers “why did this fire?” without claiming certainty beyond server data.

### SCR-08 Map

Map occupies two-thirds; synchronized alert/camera list occupies one-third. Local tiles only; marker includes icon+status and clusters expose count. Layer control toggles cameras, alerts, zones, FOV only when data exists. Missing tiles fall back to coordinate/list view. No route planning, measurement or playback if no API. Signature moment: selecting a map marker highlights the matching list row and vice versa.

### SCR-09 Event Search and SCR-10 Event Detail

Search form is collapsible and shows supported filters only. Result table supports pagination, thumbnail where authorized and query duration. Mobile uses result cards. Event detail presents source, time, category, explanation and evidence link. Loading uses skeleton rows; no results keeps filters visible; slow query reports progress only if backend supplies it. Signature moment: query and result provenance remain visible when moving into detail.

### SCR-11 Evidence Viewer and tamper demo

Player/snapshot left; metadata and integrity panel right. Integrity panel shows SHA-256, signature, chain status, anchor status and Verify action only for fields returned. Verified uses shield/seal + text; tampered uses critical red + explicit instruction not to rely on the item; cannot-verify remains distinct. Export controls include manifest status. Demo mode uses a synthetic evidence item and clearly labels it as demonstration; modified sample returns tampered only when verifier confirms. Signature moment: verification transitions to an explicit result, not a decorative animation masquerading as proof.

## Analytics and configuration

### SCR-12 Zones list / SCR-13 Zone Editor

List groups by camera and active version. Editor uses frozen frame with line/polygon handles, right-side properties (name, class filters, direction, schedule), toolbar (draw, undo, redo, save, activate). Vertex keyboard editing and numeric alternative are available. Dirty route change opens save/discard modal. Invalid geometry identifies point and reason. Version/approval/history/test/rollback controls are hidden until API support. Signature moment: normalized geometry and version are visible together before activation.

### SCR-14 ANPR / FRS / Watchlists

ANPR screen shows plate crop only if authorized, normalized text, per-character confidence when supplied, camera/time and candidate status. Search requires purpose. OCR correction and watchlist editing are disabled without audited API. FRS card prominently states “Candidate; human review required,” shows threshold/similarity only if calibrated metadata exists, and offers confirm/reject/unsure only when a decision endpoint exists. No public identity imagery or raw embedding. Watchlist enrollment requires governance/approval/expiry. Empty/denied states do not reveal hidden records.

### SCR-15 Analytics

KPI row for alert count, false-positive rate, latency and uptime; trend chart and heatmap below. Date range, timezone, comparison and sample count are explicit. Gold used only for integrity series, not general KPI. Missing/partial interval is hatched and labeled. Report scheduling/export is absent unless API supplies it.

### SCR-16 System Health

Node cards and service table show online state, version, resource metrics, camera FPS/latency/dropped frames, queue/sync and storage. Threshold indicators show exact value, unit and timestamp. Disk warning/safe mode remains persistent. Logs are read-only and secrets redacted server-side. Restart, backup, diagnostics and retention actions stay hidden until authorized endpoints exist.

### SCR-17 Model Management

Table shows model name/version, license, dataset hash, test report, signature and deployment state. Promotion review shows signing/test status and explicit impact. Upload, staged rollout and rollback are absent until APIs exist. Signature moment: verified status is text-backed, not a green dot.

### SCR-18 Users & Roles

Table presents account, assigned role, active state and MFA status when returned. Create/edit forms expose only backend-supported fields. Role changes show permissions summary and audit consequence. Deactivation is confirmed. MFA reset/force logout are hidden until endpoints exist. 403 states are generic.

### SCR-19 Ledger Console

Status panel for local chain head, pending anchor, last verified position and signer key status only if API returns them. ChainStrip visualizes sequence but includes textual hash positions. Verification range form requires start/end IDs. Anchor state is separate from local evidence verification. Key material is never displayed. UI remains read-only when ledger APIs are unavailable.

### SCR-20 Audit Log

Searchable table: actor, action, purpose, resource, time, result, request ID. Tamper-evident indicator is server-provided. Export is permission-gated, purpose-bound and audited. Empty and partial states preserve filters.

### SCR-21 Settings

Profile-level theme, density, locale, motion and notification preferences. Site settings, thresholds, retention and escalation appear only when relevant API and role exist. Unsaved changes show save/discard. Local-only preference is clearly labeled until server persistence is added.

### SCR-22 Help & About

In-app help is route-aware, searchable and local. About shows version/build only from build metadata; support bundle is disabled absent backend route. Legal/open-source notices link to local content. No remote docs dependency.

## Setup and system states

### First-run setup wizard

Future composition is a stepper: create initial admin → site name/location/timezone → time sync → add/test cameras → first zone → test event → user setup → backup settings. It is not implemented until a secure bootstrap API exists. Every step has back/continue, validation, interruption recovery and a final summary; secrets never appear in summary.

### SCR-23 403 / SCR-24 404 / SCR-25 500 / Offline / Maintenance

Use a centered original illustration, short explanation and safe next action (Back, Retry, Sign in, contact admin). 403 does not expose resource existence. 404 distinguishes invalid route from unavailable/unauthorized object with generic wording. 500 shows request ID and retry. Offline page reports local API versus HQ/WS status, stale timestamp and safe read-only options. Maintenance appears only from authoritative backend state. Signature moment: failure is clear and calm; no empty blank screen.

## Screen state requirements

| State | Design rule |
|---|---|
| Loading | Match final content geometry; no content jump; announce busy |
| Empty | Explain why empty and offer safe next action; no fake data |
| Error | Cause, request ID where safe, retry action |
| Offline | Last successful timestamp and unavailable mutation notice |
| Permission denied | Generic denial; avoid resource-existence disclosure |
| Partial | Mark each section stale/missing; never render missing as zero |
| Success | Only after server response; integrity status separately represented |
