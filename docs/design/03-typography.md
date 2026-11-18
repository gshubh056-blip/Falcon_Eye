# 03 — Typography

## Local font families

| Role | Family | Weights | License | Fallback |
|---|---|---|---|---|
| Headings / wordmark | Sora | 600, 700 | SIL OFL 1.1 | `Arial, sans-serif` |
| UI / body | Geist Sans | 400, 500, 600 | SIL OFL 1.1 | `system-ui, sans-serif` |
| Data / hashes / codes | Geist Mono | 400, 500 | SIL OFL 1.1 | `ui-monospace, monospace` |
| Hindi | Noto Sans Devanagari | 400, 500, 600 | SIL OFL 1.1 | `Nirmala UI, sans-serif` |

Fonts must be self-hosted WOFF2 with Latin and Devanagari coverage, `font-display: swap`, and no runtime external request. Preload only body regular and heading semibold when local files are installed. Font binaries are not included yet; do not reference non-existent files in a production build.

## Scale (16 px root)

| Token | Size | Line height | Intended use |
|---|---:|---:|---|
| `type-2xs` | 11 px | 16 px | Dense chart/data labels only |
| `type-xs` | 12 px | 16 px | Timestamp/secondary caption |
| `type-sm` | 13 px | 18 px | Compact controls |
| `type-ui` | 14 px | 20 px | Default control/table text |
| `type-body` | 16 px | 24 px | Body copy |
| `type-lg` | 18 px | 26 px | Emphasized body |
| `type-h4` | 20 px | 28 px | Section title |
| `type-h3` | 24 px | 32 px | Page subsection |
| `type-h2` | 30 px | 38 px | Page title on desktop |
| `type-h1` | 40 px | 48 px | Login or major heading |
| `type-display` | 56 px | 64 px | Sparse brand/empty-state display |

Use Sora for headings and Geist Sans for all other interface copy. Use no more than three font weights on one screen. Paragraph line length is at most 70 characters.

## Data typography

Use Geist Mono with `font-variant-numeric: tabular-nums` for timestamps, counters, coordinates, FPS, confidence, plate/OCR strings and hashes. Hashes may truncate in the middle with full value available through a labeled copy action; do not shrink them below 12 px. Store and transmit normalized values; localize only their display.

## Hindi and localization

Hindi uses Noto Sans Devanagari with line-height increased by at least 8% from Latin body style and a 1 px size increase where required. Never clip matras; controls may grow vertically and labels wrap. Do not reduce font size to force a one-line fit. Test mixed Latin IDs and Devanagari in tables, dialogs, badges and controls. English fallback is used if a translation key is missing.

## Distance and density

Wall mode multiplies UI sizes by 1.25, with 16 px minimum for text needed at 2–3 m. Compact is operator default; it may reduce row padding but not text readability or touch targets on touch screens.
