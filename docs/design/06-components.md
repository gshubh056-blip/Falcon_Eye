# 06 — Components

This is the visual/interaction contract for the components in `WEB_FLOW.md`. All visual values come from design tokens. Components must not invent backend success, user permissions or state. The dashboard package is not yet scaffolded; this file is the implementation specification, not a component-existence claim.

## Shared state contract

Where applicable, every interactive component supports:

| State | Visual treatment | Behavior |
|---|---|---|
| Default | Base surface, 1 px token border | Ready |
| Hover | `surface-3`/border-default | Pointer only; no meaning conveyed by hover alone |
| Focus-visible | 2 px cyan ring, 2 px offset | Never removed; reachable by keyboard |
| Active/pressed | Pressed token; no layout shift | Action is pending until server confirms |
| Selected | Cyan/neutral selected surface plus selected marker | Selection announced |
| Disabled | Disabled affordance and readable explanation where needed | Not focusable unless an explanatory disabled control pattern is used |
| Loading | Stable dimensions, spinner/skeleton and accessible busy state | Prevent duplicate submission |
| Error | Error text/icon and programmatic association | User can correct or retry |
| Success | Text/icon; gold only for integrity | Must be backed by confirmed result |
| Read-only | Normal readable content and read-only cue | No misleading hover or action affordance |

Use `aria-invalid`, `aria-describedby`, `aria-busy`, `aria-expanded`, `aria-selected` and live-region announcements as appropriate. Dialogs trap focus, return focus to trigger, close on Escape unless action is in a non-dismissible transaction, and have a visible close/cancel control. Touch targets are at least 44 px; desktop compact targets at least 32 px.

## Interaction components

| Component | Anatomy / variants / sizes | Keyboard and accessibility |
|---|---|---|
| Button | Label + optional leading/trailing icon. Primary cyan, secondary outlined, ghost, danger, gold-integrity-only, icon-only. Small/medium/large. | Native button; Enter/Space; icon-only has `aria-label`; loading uses `aria-busy`. |
| IconButton | Icon, hit area, optional tooltip. Neutral/active/danger. | Native button, accessible name, tooltip not sole label. |
| Input | Label, control, optional prefix/suffix, hint/error. Text/search/number. | Label association; Enter submits only when form expects it; errors linked. |
| PasswordInput | Input plus reveal toggle and strength/status text where supported. | Toggle announces “Show password/Hide password”; value never logged. |
| Select | Label, selected value, option list, error. Single/multiple only when API supports it. | Native select preferred; otherwise listbox semantics and arrow navigation. |
| Combobox | Input, result list, loading/empty state. | WAI-ARIA combobox; arrows, Enter, Escape; async status announced. |
| DateTimeRangePicker | Start/end, timezone display, quick ranges only if supported. | Keyboard calendar navigation; inputs expose validation and timezone. |
| Slider | Track, thumb, label/value, min/max. | Arrow keys adjust; Home/End bounds; `aria-valuetext`. |
| Switch | Label, track, checked state and optional helper. | Space toggles; `role=switch`; state is explicit text too. |
| Checkbox | Box, label, optional mixed state. | Space toggles; native checkbox; mixed only when justified. |
| Radio | Group label, options and description. | Arrow keys within group; fieldset/legend. |
| Tabs | Tab list, active tab, panel. | Arrow/Home/End and correct tab/tabpanel IDs. |
| SegmentedControl | Connected mutually exclusive options. | Radio-group semantics or tabs depending on content change. |
| Tooltip | Short noninteractive description. | Appears on hover and focus; Escape dismisses; never contains required instructions. |
| Popover | Trigger, anchored panel, optional form/content. | Focus management, Escape, outside-click handling, labeled region. |
| Dropdown menu | Trigger and action list with destructive separators. | Menu arrow navigation; actions named; confirmation for destructive items. |
| Context menu | Target-specific actions. | Keyboard alternative and visible equivalent; not pointer-only. |
| Dialog/Modal | Title, content, footer actions; small/medium/large. | Focus trap, title/description, Escape behavior and return focus. |
| Confirm-destructive dialog | Consequence summary, cancel, danger confirmation; type-to-confirm for irreversible operations. | Confirmation button disabled until required phrase matches; announce consequence. |
| Drawer | Side panel with title, content and close. | Modal behavior on narrow screens; focus returns to trigger. |
| Toast | Icon, title/body, optional action and close. | Polite live region; no critical information only in transient toast. |
| Banner | Severity icon/label, message, optional action/dismiss. | Persistent alert uses `role=alert` only for urgent; ordinary uses status. |
| Badge | Small labeled state. Neutral, success, warning, error, info. | Text remains present; do not use color-only dot. |
| SeverityBadge | Severity icon shape + exact label + color. | Accessible text names the exact severity; position consistent. |
| StatusDot | Dot + adjacent status text. Online/offline/syncing/unknown. | Dot decorative; text conveys state. |
| Chip/Tag | Label, optional removable control. | Remove button has accessible name; static tag is not a button. |
| Avatar | Initials or original generic silhouette; role/state may be adjacent. | Decorative when name shown; otherwise labeled. Never use face crops as avatars. |
| Card | Header, content, optional actions. Standard, interactive, selected. | Interactive card uses one semantic link/button; nested controls avoided. |
| KPI Card | Label, tabular value, delta/context, optional sparkline; chamfer top-right. | Name/value announced together; no color-only trend. |
| AlertCard | Severity icon/label, title, source/time, state, action. Active card chamfer. | Entire card not an unlabeled click target; actions separate and named. |
| AlertRow | Compact list row with selected/unread/escalated state. | Roving focus or row link; updates do not steal focus. |
| DataTable | Sticky header, sorting, filters, virtual rows, density and selection. | Semantic table; sort direction announced; virtualized row order remains navigable. |
| Pagination | Page/size, previous/next, total if known. | Buttons named and disabled at bounds; page changes announced. |
| Timeline | Timestamp, actor, action and state; chronological. | Ordered list; text timestamps, no color-only actions. |
| Stepper/Wizard | Current step, completed steps and body. | Current step announced; validate before advance; preserve entered safe data. |
| Skeleton | Shape matches content. | `aria-hidden`; containing region announces loading. No shimmer with reduced motion. |
| EmptyState | Original local illustration, title, explanation, optional action. | Heading and action in reading order; illustration decorative. |
| ErrorState | Cause, safe request ID, retry/support action. | `role=alert` for blocking error; never render stack trace. |
| ProgressBar | Label, value/indeterminate state. | `progressbar` value range or busy state; no fabricated completion. |
| Spinner | Small, medium, large. | Decorative plus nearby loading label; reduced motion uses static glyph. |

## Operations, video, integrity and navigation components

| Component | Anatomy / variants / states | Keyboard and accessibility |
|---|---|---|
| VideoTile | Video surface, camera/time/status header, layer toggles, action menu; 1/4/9/16 grid sizes. Live cyan hairline, alert severity edge, offline dashed neutral. | Tile selection by keyboard; status text separate from video; never blur. |
| DetectionOverlay | Corner-bracket boxes, class label, confidence when approved, trail, zone fill/dashed outline. | Canvas content has equivalent accessible detection summary; timestamp aligns with frame. |
| ZoneEditorCanvas + toolbar | Frozen frame, normalized line/polygon, vertices, undo/redo, save/activate and dirty state. | Keyboard vertex selection/move and numeric coordinate alternative; canvas role/name/help. |
| PTZ pad | Directional controls, stop, speed if supported. | Large targets; press-and-hold has reliable stop on release/focus loss; stop always available. |
| Timeline scrubber | Clip duration, playhead, event markers and frame-step buttons. | Keyboard seek and frame-step; current time announced; respect reduced motion. |
| MapMarker/Cluster/FOV cone | Marker icon, status/severity label, accessible cluster count and optional camera cone. | List alternative, keyboard activation, no hidden alert in marker-only map. |
| ChainStrip | Ordered hash blocks, link state and chain position. | Text summary and ordered list; color/gold not sole integrity cue. |
| IntegritySeal | Verified/Tampered/Pending/Cannot verify. Seal icon, explicit label, timestamp. | Exact state announced; tampered is urgent; gold only verified/ledger motif. |
| PlateChip | OCR text, confidence and candidate status. | String is inert text; never HTML; purpose and access controls outside chip. |
| FaceMatchCard | Candidate label, similarity, limitations and human review actions. | “Candidate, not confirmed identity” always visible; accessible confirm/reject/unsure labels. |
| ConfidenceMeter | Numeric percentage and optional visual meter. | Numeric value exposed; do not imply probability calibration unless model metadata says so. |
| SLA Timer | Time elapsed/remaining, threshold and status label. | Updates throttled and not announced every second; exact underlying status available. |
| HealthTile + Sparkline | Metric name, current value, units, trend and stale timestamp. | Sparkline decorative; accessible text summary and units. |
| Charts | Line/bar/donut/heatmap with sparse grid and text legend. | Data table alternative; patterns/markers; missing is not zero. |
| CommandPalette | Searchable command list; Ctrl+K per web-flow shortcut specification. | Dialog/listbox semantics, keyboard navigation; permission filters server-confirmed. |
| ShortcutHelp overlay | Searchable shortcut table and scope notes. | `?` opens; Escape closes; editable-field shortcut conflicts documented. |
| LanguageSwitch | English/Hindi selection. | Native select or radiogroup; locale name spoken natively. |
| ThemeSwitch | Obsidian/Ivory/High Contrast/Night-dim. | Accessible names and selected state; no reload/data loss. |
| NotificationTray | Unread count, grouped alert updates, history and preferences. | Focusable list; critical alert not dismissed by DND; live announcements throttled. |
| OfflineBanner | Local API/HQ/WS state, last update and retry when safe. | Persistent status region; distinct local vs HQ outage. |
| LockScreen | Session lock state and reauthentication control. | Visible reason/session state; backend policy required before implementation. |
| FileDropzone | Accepted type/size, upload progress, validation. | Keyboard browse alternative; server validates; no implicit upload. |
| CodeBlock/HashDisplay | Monospace value, middle truncation, copy confirmation. | Full value accessible or expandable; copy button label includes value context. |
| Breadcrumbs | Route parents and current page. | `nav` landmark and current-page indication. |
| SideNav | 72/248 px collapsed/expanded, grouped route links. | Labeled navigation; active item `aria-current`; no route hidden only by color. |
| TopBar | Site, clock, node/WS state, counters, user menu. | Logical focus order; urgent status announced once and persistent. |

## Component state matrix

All components above use the shared state contract where the state is meaningful. This matrix records required exceptions so galleries and implementation tests are explicit:

| Component group | Required state examples |
|---|---|
| Button, IconButton, Input, PasswordInput, Select, Combobox, DateTimeRangePicker, Slider, Switch, Checkbox, Radio | Default, hover, focus-visible, active, selected/checked, disabled, loading when async, error, success, read-only |
| Tabs, SegmentedControl, Dropdown, Context menu, Dialog, Drawer, Popover, Tooltip, CommandPalette, ShortcutHelp | Closed/default, open, focus-visible, selected item, disabled item, empty/loading/error content, read-only action |
| Toast, Banner, Badge, SeverityBadge, StatusDot, Chip, Avatar | Default, hover/focus if interactive, selected/removable, disabled, success/error/warning/info, read-only |
| Card, KPI Card, AlertCard, AlertRow, DataTable, Pagination, Timeline, Stepper | Loading, empty, partial, error, offline/stale, selected, disabled action, success result |
| VideoTile, DetectionOverlay, PTZ pad, Timeline scrubber | Live, buffering, reconnecting, offline, no signal, privacy masked, night metadata, action pending/error, read-only |
| Zone editor, MapMarker/Cluster/FOV cone | Default, selected, edit/dirty, invalid geometry, saving, saved, denied, offline, read-only |
| ChainStrip, IntegritySeal, CodeBlock/HashDisplay | Verified, tampered, pending, cannot verify, loading, error; copy success/error |
| PlateChip, FaceMatchCard, ConfidenceMeter | Candidate, low confidence, unavailable, human confirmed only when server-confirmed, rejected/unsure, access denied |
| HealthTile, Sparkline, Charts, ProgressBar, Spinner, Skeleton, EmptyState, ErrorState | Loading, empty, partial, stale, offline, error, reduced-motion equivalent |
| LanguageSwitch, ThemeSwitch, NotificationTray, OfflineBanner, LockScreen, FileDropzone | Default, selected, permission denied, offline, loading, error, success, read-only |

## Usage example

```tsx
<SeverityBadge severity="critical" label="Critical" />
<Button variant="primary" loading={submitting} aria-busy={submitting}>
  Acknowledge alert
</Button>
<IntegritySeal status="verified" label="Evidence integrity verified" />
```

Props and status enums must be generated from the API contract where one exists. The example documents semantic intent; it is not evidence that these React components have already been implemented.
