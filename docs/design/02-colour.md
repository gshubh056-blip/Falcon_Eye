# 02 — Color

## Color rules

Obsidian is the default operations theme. Ivory is the secondary theme. High Contrast is an accessibility mode. Night-dim is a low-luminance variant. CSS variables are defined in `apps/dashboard/src/design/tokens.css`.

- Radar Cyan is live, active, selected and primary-action color.
- Seal Gold is restricted to integrity, ledger, seal and evidence verification. It is never a severity.
- Severity pairs color with text label, icon shape and stable location.
- Do not use disabled colors for required instructions or text. Keep disabled controls understandable and explicitly unavailable.
- A colored border/icon may use the severity color if its adjacent-surface contrast is at least 3:1. Body text always uses a text token.

## Obsidian palette (locked)

| Token | Value | Use |
|---|---|---|
| `canvas` | `#060A11` | Wall/app background |
| `base` | `#0A101A` | Page background |
| `surface-1` | `#0E1623` | Cards/panels |
| `surface-2` | `#131D2E` | Raised cards/inputs |
| `surface-3` | `#192640` | Hover/selected rows |
| `border-subtle` | `#1C2A40` | Hairlines |
| `border-default` | `#263650` | Component borders |
| `border-strong` | `#364A6B` | Dividers |
| `text-primary` | `#EAF0F8` | Main text |
| `text-secondary` | `#A3B3CB` | Supporting text |
| `text-tertiary` | `#70829E` | Secondary timestamp/hint |
| `text-disabled` | `#4A5A74` | Nonessential disabled decoration only |

## Brand and semantic colors

| Token | Value | Meaning |
|---|---|---|
| `cyan-400` | `#3CD7E8` | Live focus/active border |
| `cyan-500` | `#1FC0D4` | Main active/primary |
| `cyan-600` | `#12A0B5` | Pressed/strong active |
| `on-brand` | `#03181C` | Text/icon on cyan action fill |
| `gold-300` | `#E9CB86` | Verified seal highlight |
| `gold-400` | `#D9AE55` | Gold gradient mid |
| `gold-500` | `#C2963B` | Ledger accent |
| `success` | `#2FD08A` | Online/success |
| `offline` | `#70829E` | Offline |
| `warning` | `#F4C23E` | Warning (with label/icon) |

Seal gradient: `linear-gradient(135deg, #E9CB86 0%, #C2963B 55%, #E9CB86 100%)`. Use only for decorative integrity seal edge, never small text.

## Severity palette

| Level | Obsidian | Ivory | Shape |
|---|---|---|---|
| Critical | `#FF4D5E` | `#D6293F` | Filled octagon/siren |
| High | `#FF8A3D` | `#D9650F` | Triangle |
| Medium | `#F4C23E` | `#B88A00` | Diamond |
| Low | `#4DA3FF` | `#1F6FD1` | Circle |
| Info | `#8FA1BD` | `#5B6E8B` | Outlined circle |

Use dark-text label on light severity indicators and light-text label on dark indicators. The severity swatch itself is not used as normal-size text. States: tampered uses critical red; pending uses neutral/cyan with “Pending”; syncing uses cyan; verified uses success plus Seal Gold shield/seal; do not make gold mean generic success.

## Ivory palette (locked)

| Token | Value | Use |
|---|---|---|
| `canvas` | `#EEF2F7` | App background |
| `surface-1` | `#FFFFFF` | Main cards |
| `surface-2` | `#F6F8FB` | Raised areas |
| `border-default` | `#D5DDE8` | Borders |
| `text-primary` | `#0B1424` | Main text |
| `text-secondary` | `#44556F` | Required supporting text |
| `text-tertiary` | `#6B7C95` | Nonessential label/icon only on white |
| `brand` | `#0B8CA0` | UI accents, non-text surfaces |
| `gold` | `#9A7424` | Integrity icon/mark; text remains primary |
| `success` | `#11875A` | Online/success |

## High Contrast and Night-dim

High Contrast uses black `#000000` canvas/surface, white `#FFFFFF` text, 2 px white/black boundaries, cyan `#00E5FF` focus/active, and visible system focus. Severity uses the same icons and labels plus the theme's severity palette; forced-colors relies on system colors and outlines. Do not suppress `forced-colors`.

Night-dim uses Obsidian layout, warmed text (`#E8E3D8`) and muted cyan (`#57B7BE`), lowered decorative luminance, and no pure white text. Its exact tokens are in CSS and must pass contrast checks before release.

## Measured contrast

WCAG 2.1 ratio formula: `(Llighter + .05) / (Ldarker + .05)`. Normal text target is 4.5:1; large text and non-text controls target 3:1. Results below use provided sRGB values:

| Foreground / background | Ratio | Result / use |
|---|---:|---|
| Obsidian primary / canvas | 17.29:1 | AAA text |
| Obsidian primary / surface-1 | 15.82:1 | AAA text |
| Obsidian secondary / canvas | 9.32:1 | AAA text |
| Obsidian secondary / surface-1 | 8.52:1 | AAA text |
| Obsidian tertiary / canvas | 5.08:1 | AA normal text |
| Obsidian tertiary / surface-1 | 4.64:1 | AA normal text |
| Obsidian disabled / surface-1 | 2.60:1 | Fail text; nonessential decoration only |
| Cyan 400 / canvas | 11.40:1 | AA text mathematically; keep for accents |
| Cyan 500 / canvas | 9.01:1 | AA text mathematically; keep for accents |
| Cyan 600 / canvas | 6.35:1 | AA text mathematically; keep for accents |
| Gold 300 / canvas | 12.60:1 | Accent; integrity only |
| Gold 400 / canvas | 9.57:1 | Accent; integrity only |
| Gold 500 / canvas | 7.29:1 | Accent; integrity only |
| Obsidian Critical / canvas | 6.11:1 | AA text mathematically; still pair with label/icon |
| Obsidian High / canvas | 8.45:1 | AA text mathematically; still pair with label/icon |
| Obsidian Medium / canvas | 11.93:1 | AA text mathematically; still pair with label/icon |
| Obsidian Low / canvas | 7.55:1 | AA text mathematically; still pair with label/icon |
| Obsidian Info / canvas | 7.55:1 | AA text mathematically; still pair with label/icon |
| Ivory primary / canvas | 16.39:1 | AAA text |
| Ivory secondary / surface-1 | 7.57:1 | AAA text |
| Ivory tertiary / surface-1 | 4.25:1 | Fail normal text; nonessential only |
| Ivory brand / surface-1 | 3.98:1 | UI accent; not normal text |
| Ivory gold / surface-1 | 4.29:1 | Integrity accent; not normal text |
| Ivory Critical / surface-1 | 4.94:1 | AA text mathematically; pair with shape |
| Ivory High / surface-1 | 3.61:1 | UI indicator only; label uses primary |
| Ivory Medium / surface-1 | 3.15:1 | UI indicator only; label uses primary |
| Ivory Low / surface-1 | 4.94:1 | AA text mathematically; pair with shape |
| Ivory Info / surface-1 | 5.19:1 | AA text mathematically; pair with shape |
| Obsidian Success / canvas | 9.92:1 | AA text mathematically |
| Ivory Success / surface-1 | 4.53:1 | AA normal text |

## Color-vision and usage checks

Protanopia/deuteranopia can reduce red/green distinction; tritanopia can reduce blue/yellow distinction. Verify each severity badge in grayscale and with simulation. Severity remains identifiable from shape, label, and list position. Do not put red/green alone on a map or chart. Use pattern/marker shape in heatmaps and severity series.
