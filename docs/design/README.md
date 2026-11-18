# FALCON UI/UX Design System

**Design direction:** Obsidian Command  
**Version:** 1.0  
**Status:** Design baseline for the dashboard; not a claim that the dashboard is implemented.

## Purpose

This directory turns `docs/PRD.md`, `docs/TRD.md` and `docs/WEB_FLOW.md` into a shared visual and interaction contract. It is for product, design, frontend, QA, accessibility, security and operations contributors.

The primary interface is a calm, precise, night-ready command console. Use Obsidian surfaces, Radar Cyan for active/live information, and Seal Gold only for evidence integrity, ledger and verification. Use severity color only alongside a label, icon shape and stable position. Operator workflows remain human-controlled: recognition results are candidates, never autonomous decisions.

## Source-of-truth and build path

- Product behavior and priority: `../PRD.md`.
- API, protocol and repository path: `../TRD.md`.
- Screens, actions, states, flows, messages and test IDs: `../WEB_FLOW.md`.
- This design system controls visual tokens, component anatomy and page composition. It does not invent an API contract.
- The TRD specifies `apps/dashboard`; therefore frontend foundation files belong there, not in a parallel `web/` application. No dashboard package manifest currently exists, so these tokens are framework-independent and do not imply a runnable app.
- Runtime assets must be local. No CDN fonts, remote images, third-party map tiles or internet-dependent icon requests.

## Documents

| File | Purpose |
|---|---|
| [01-brand-and-principles.md](./01-brand-and-principles.md) | Identity, logo construction, voice, control-room principles |
| [02-colour.md](./02-colour.md) | Theme palettes, semantic use, measured contrast, color-vision guidance |
| [03-typography.md](./03-typography.md) | Self-hosted font families, type scale, Hindi rules |
| [04-layout-spacing-elevation.md](./04-layout-spacing-elevation.md) | Grids, breakpoints, density, surfaces and elevation |
| [05-iconography-illustration-motion-sound.md](./05-iconography-illustration-motion-sound.md) | Icons, custom illustrations, animation and notification sound |
| [06-components.md](./06-components.md) | Component anatomy, variants, states, keyboard and ARIA behavior |
| [07-screens.md](./07-screens.md) | Screen-level compositions and visual states mapped to SCR IDs |
| [08-accessibility-and-quality.md](./08-accessibility-and-quality.md) | Accessibility, visual review and performance criteria |
| [DECISIONS.md](./DECISIONS.md) | Decisions, rationale and rejected alternatives |
| [LICENSES.md](./LICENSES.md) | Third-party asset and library license register |

## Token and asset implementation

The initial framework-independent tokens are in `../../apps/dashboard/src/design/tokens.css` and `tokens.ts`. They are the source for CSS and canvas/chart consumers. The dashboard package is not scaffolded yet, so Tailwind, Radix, Lucide, Motion, charts, maps, component gallery and build commands are intentionally not configured or claimed as passing.

To use the tokens, load `tokens.css` once at the application entry, set `data-theme="obsidian"` on the root element, then optionally set `data-density="compact"` or `data-display="wall"`. Components must use token variables rather than hard-coded colors, type sizes, spacing, radii, shadows or z-index values.

Run the current contrast validation with `python scripts/check_contrast.py`. A `npm run design:check` command can be added when a Node.js package manifest exists.

## Design review gate

Before a component or screen is called complete:

1. Link it to the relevant SCR/CMP/STA/MSG/ACT/RT IDs in `WEB_FLOW.md`.
2. Verify keyboard, screen reader, reduced-motion and forced-colors behavior.
3. Check all supported themes and English/Hindi text fit.
4. Verify error, offline, stale, permission-denied and partial-data states.
5. Confirm no remote asset requests, exposed camera credentials, biometric data or tokens.
6. Measure contrast and test severity without color.
7. Record unsupported backend capabilities as gaps; never simulate a successful operation.

See `DECISIONS.md` for assumptions resulting from the repository having no dashboard source or package configuration.
