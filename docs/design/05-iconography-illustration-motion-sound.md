# 05 — Iconography, Illustration, Motion and Sound

## Iconography

Lucide is the general icon base when installed locally: 1.5 px stroke, 20 px default, 16 px dense and 24 px prominent, consistent rounded caps. Icons require accessible labels unless decorative. Never use emoji as an icon. Use text labels for critical actions.

Custom icon set (SVG/React component names):

| Domain | Icons |
|---|---|
| Brand | `FalconMark`, `RadarSweep` |
| Perimeter | `VirtualFence`, `Trajectory`, `Loitering`, `AbandonedObject` |
| Analytics | `Plate`, `FaceMatch`, `NightThermal` |
| Integrity | `LedgerSeal`, `ChainLink`, `IntegrityVerified`, `IntegrityTampered`, `IntegrityPending` |
| Operations | `EdgeNode`, `OfflineMode`, `Siren` |

Severity shapes: octagon, triangle, diamond, circle, outlined circle. Keep the corresponding word label adjacent.

## Illustrations and local SVG assets

Original SVG line-art uses cyan and neutral strokes; gold may appear only in ledger/integrity artwork. No real-person photos or stock images.

| Asset | Description |
|---|---|
| `contour-pattern.svg` | Subtle topographic contour lines |
| `login-hero.svg` | Abstract terrain bands and static radar field |
| `empty-alerts.svg` | Quiet radar ring and “All clear” context |
| `empty-cameras.svg` | Camera outline with connection cue |
| `empty-results.svg` | Search reticle and empty grid |
| `empty-offline.svg` | Edge node with disconnected link |
| `empty-error.svg` | Broken panel/repair cue |
| `empty-403.svg` | Access shield, not a padlock-as-security guarantee |
| `empty-404.svg` | Missing route marker |
| `empty-500.svg` | Service status outline |
| `empty-maintenance.svg` | Node maintenance indicator |
| `loading-mark.svg` | Falcon mark draw-on loading, static fallback |

Animations are decorative; content and meaning remain available if SVGs do not load.

## Data visualization

Use 1.5 px lines, subtle area fills, sparse gridlines and tabular labels. Cyan is the primary series; Seal Gold only represents ledger/integrity metrics. Severity series use the palette plus distinct markers/patterns. Heatmaps use a perceptually ordered dark-to-cyan-to-amber ramp and an explicit legend; missing data is not zero.

## Motion tokens

Durations: 120 ms micro, 180 ms control, 240 ms panel, 400 ms route/illustration. Easing: `cubic-bezier(.2,.8,.2,1)`. Spring only for direct manipulation such as drag/drop, never for alert urgency.

| Motion | Spec |
|---|---|
| Alert insertion | 180 ms opacity/translate, no list jump; no repeated animation on update |
| Critical indicator | Soft ring pulse, 1.6 s cycle, no flash; static octagon in reduced-motion |
| KPI count | 240 ms number transition; respect reduced motion |
| Loading | Static skeleton by default; gentle shimmer only if motion allowed |
| Evidence verification | One-time chain progression then seal state; final text result remains |
| Tamper result | One 120 ms horizontal nudge, then stable red state; never loops |
| Login radar | 60 s loop maximum, pause when tab hidden, static when reduced-motion |

No animation may flash more than three times per second. Every animation has a static equivalent under `prefers-reduced-motion` and in the in-app Reduce motion setting.

## Sound

Use Web Audio oscillator tones only after explicit user gesture and preference. Default volume is low and alerts remain visual regardless of sound.

| Severity | Suggested tone | Duration |
|---|---|---:|
| Info | 660 Hz sine, single soft tone | 100 ms |
| Low | 520 Hz sine, single tone | 120 ms |
| Medium | 440 Hz sine, two tones 100 ms apart | 240 ms total |
| High | 360 Hz triangle, two soft tones | 280 ms total |
| Critical | 300 Hz sine plus 600 Hz harmonic, three short tones | 360 ms total |

Do not sound on every update of the same alert. DND suppresses non-critical sounds; it never hides a critical alert. Provide mute and volume controls; critical visual presentation cannot be muted. Handle autoplay block with explanatory text, not silent failure.
