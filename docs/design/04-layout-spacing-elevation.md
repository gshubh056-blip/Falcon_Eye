# 04 — Layout, Spacing and Elevation

## Grid and breakpoints

The content grid has 12 columns, 24 px desktop gutters, and a 1920 px maximum content width. Narrow screens collapse columns rather than forcing horizontal scrolling; data tables may have a labeled horizontal scroll region.

| Range | Layout |
|---|---|
| Wall: `>=2560px` | Wall density, expanded operational surfaces, up to 16 selected tiles subject to measured stream capacity |
| Desktop: `>=1440px` | Expanded navigation and 12-column dashboard |
| Laptop: `>=1024px` | Collapsible navigation; preserve alert list/detail |
| Tablet: `>=768px` | Compact navigation and single detail drawer |
| Mobile: `<768px` | Single-column review; prioritize alert, evidence metadata and search |

Navigation width is 72 px collapsed and 248 px expanded. Top bar is 56 px; status bar is 28 px. Wall mode enlarges these according to 1.25 scale.

## Spacing

Base grid is 4 px. Tokens: `space-0.5=2px`, `space-1=4px`, `space-2=8px`, `space-3=12px`, `space-4=16px`, `space-5=20px`, `space-6=24px`, `space-8=32px`, `space-10=40px`, `space-14=56px`, `space-20=80px`.

Comfortable uses 16 px default row vertical padding; Compact uses 8 px; Wall uses at least 16 px. Density changes padding and layout, never hiding severity, state, timestamps or action labels.

## Radius and signature silhouette

Controls: 6 px; cards: 10 px; panels/dialogs: 14 px; pills/avatars: 999 px. KPI/hero cards and active alert card use a 10 px top-right chamfer via a decorative pseudo-element or clip path. Keep focus outline outside the clipping path. Avoid chamfering every component.

## Surfaces and elevation

| Level | Surface/border | Shadow |
|---|---|---|
| 0 | Canvas, no shadow | none |
| 1 | Surface-1, subtle border | `0 1px 2px rgba(0,0,0,.24)` |
| 2 | Surface-2, default border | `0 4px 12px rgba(0,0,0,.24)` |
| 3 | Surface-2, strong border | `0 12px 28px rgba(0,0,0,.32)` |
| 4 | Modal/popover, strong border | `0 20px 48px rgba(0,0,0,.42)` |

Cards also use a faint top inner highlight `inset 0 1px 0 rgba(255,255,255,.04)`. Borders take precedence over shadows.

## Glass and performance mode

Top bar, side panels and modals may use surface-2 at 72% with 12 px backdrop blur. Use a solid token surface when `backdrop-filter` is unsupported, reduced transparency is requested, or performance mode is enabled. Never blur live video tiles or put a translucent decorative pattern over evidence.

## Layering

Use ordered z-index tokens: base 0, sticky 10, nav 20, popover 30, modal 40, toast 50, critical global banner 60. Do not create arbitrary local z-index values. Critical banner cannot be occluded by an open drawer.
