# 08 — Accessibility and Quality

## WCAG 2.1 AA checklist

- [ ] Every action is keyboard reachable and has visible 2 px cyan focus ring with 2 px offset; focus is never removed.
- [ ] Touch targets are at least 44×44 px; desktop compact controls are at least 32×32 px.
- [ ] Text contrast is at least 4.5:1; large text and non-text UI boundaries are at least 3:1.
- [ ] Severity uses label + icon shape + color + stable placement.
- [ ] Page has landmarks, one H1, ordered headings, meaningful labels, table headers and breadcrumb navigation.
- [ ] Dialogs trap/restore focus correctly; menus and comboboxes use expected keyboard interaction.
- [ ] Critical alert updates are announced once in an assertive region; routine updates use polite announcements and are throttled.
- [ ] No required meaning is available only through hover, sound, color, animation or video.
- [ ] Reduced motion setting and `prefers-reduced-motion` stop nonessential animation and use static equivalents.
- [ ] `forced-colors: active` preserves boundaries, focus, selected state and severity labels; do not disable system colors.
- [ ] Layout and text remain usable at 200% zoom and narrow viewport without clipped Hindi matras.
- [ ] Video information has text alternative; charts have a data table or equivalent summary.
- [ ] CAPTCHA, timing or auto-logout does not create inaccessible task completion barriers; session policy follows backend contract.

## Color and vision review

Test Obsidian, Ivory, High Contrast and Night-dim. Review protanopia, deuteranopia, tritanopia and grayscale. Confirm severity shapes remain distinguishable, selected/focused states remain visible, error and verified states have text, and Gold is only an integrity cue. Review actual component foreground/background pairs, not palette samples alone.

## Visual QA

- [ ] Compare desktop at 1440×900, 1920×1080 and wall at 2560×1440.
- [ ] Test laptop at 1366×768, tablet at 768 px and mobile below 768 px.
- [ ] Check English and Hindi, long camera names, long plate strings, hashes, large counters and long error text.
- [ ] Verify no layout shift on live inserts, loading-to-data transition or route change.
- [ ] Check camera state borders and overlay registration using synthetic test stream.
- [ ] Verify modal/drawer stacking, critical banner visibility and keyboard focus return.
- [ ] Check all screen states: loading, empty, error, offline, denied, partial and read-only.
- [ ] Confirm snapshots/clips never receive backdrop blur or decorative overlays.
- [ ] Check reduced motion and high contrast on Login, Live Wall, Alert Detail, Zone Editor and Evidence Viewer.
- [ ] Block network access and verify app fonts, icons, SVGs, map style/tiles and help still load locally.

## Performance and runtime budgets

| Area | Target |
|---|---|
| Scrolling lists | 60 fps target on reference desktop; virtualize long alert/event tables |
| Live tiles | Maximum 16 selected tiles is a UI ceiling, not a hardware guarantee; measured capacity controls enablement |
| Bundle | Initial JS <= 300 KiB gzip target; lazy route chunks <= 200 KiB gzip each, excluding separately measured video/map/chart libraries |
| Layout shift | CLS <= 0.1 target; reserve media and chart dimensions |
| UI response | Local interactions <=100 ms target; alert list update follows PRD <=2 s source-to-UI target |
| Memory | Bound caches and release video tracks/listeners on route change; 24-hour soak required |
| Network | No third-party runtime requests; low-bandwidth mode prioritizes metadata/snapshots and defers clips |

These are frontend targets; benchmark hardware/browser before claiming achieved results.

## Pre-release design review

- [ ] PRD/TRD/WEB_FLOW requirements and IDs traced to screens, actions and tests.
- [ ] No unsupported API operation is represented as available.
- [ ] No plain text camera credentials, tokens, private keys, raw face embeddings or unnecessary biometric data.
- [ ] Face/plate search is role/purpose/audit gated; face candidate is not presented as confirmed identity.
- [ ] Evidence verification distinguishes verified, tampered, pending and cannot verify.
- [ ] Local/offline state distinguishes edge service from HQ synchronization.
- [ ] All fonts/assets are locally bundled and license files are in the distribution.
- [ ] Browser security headers, CSP, safe text rendering, CSRF/token handling and signed downloads are reviewed with backend.
- [ ] Screens tested with keyboard, screen reader, zoom, touch, Hindi and forced-colors.
- [ ] Contrast script passes for text pairs; manual component review passes for non-text boundaries.
- [ ] Visual snapshots reviewed for all themes and wall-size layout.
- [ ] No critical/high accessibility or security findings remain.

## Quality status

The repository currently has no dashboard package, test runner or installed assets. Therefore component-level axe checks, screenshot comparison, bundle measurement, design route, lint and build are not yet runnable. Add these gates when `apps/dashboard` is scaffolded; do not report them as passing in advance.
