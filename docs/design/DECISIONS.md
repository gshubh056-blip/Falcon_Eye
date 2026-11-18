# Design Decisions

| ID | Decision | Reason | Alternative rejected |
|---|---|---|---|
| DD-01 | Adopt the locked “Obsidian Command” direction and locked values from the master prompt unless measured contrast requires a change. | Consistent brand language for a 24×7 control-room UI. | Introducing a second visual direction or generic component-library theme. |
| DD-02 | Follow the TRD path `apps/dashboard`, not the prompt's `/web` path. | The TRD is authoritative for repository structure and names `apps/dashboard`. | Creating two competing dashboard roots. |
| DD-03 | CSS custom properties are the token source; TypeScript exports corresponding values for chart/canvas use. | Theme changes remain runtime-selectable and visual styling has one source. | Duplicating unrelated literal palettes in each component. |
| DD-04 | Keep initial foundation framework-independent; do not install packages or create a partial Vite app without a package manifest/request to scaffold. | The repository currently contains documentation only; TRD identifies React/TypeScript but no concrete frontend app files. | Claiming an unconfigured `/design-system` route or untested components exist. |
| DD-05 | Gold is reserved for integrity, ledger and evidence verification. | Protects its semantic meaning and avoids competition with alert severity. | Gold as a general premium button or high-severity color. |
| DD-06 | Severity always uses label, icon shape and position in addition to color. | Accessibility and quick recognition under color-vision deficiency. | Color-only severity. |
| DD-07 | Hindi strings remain text resources and use Noto Sans Devanagari when locally available. | Correct shaping and line-height without translating identifiers or machine enums. | Transliteration or shrinking Hindi to fit. |
| DD-08 | Brand colors remain locked as accents; normal-sized text on a brand/severity color uses a tested foreground/surface combination. | Several specified accents do not meet 4.5:1 as text on white or dark surfaces. | Treating accent color as automatically readable text. |
| DD-09 | Nonessential disabled controls may be subdued, but required disabled-state text retains readable contrast. | Disabled controls still need to be understandable. | Using very low-contrast text for required information. |
| DD-10 | No live video blur, remote tile, external font or CDN request. | Edge/offline availability, video performance and privacy. | Network-dependent decoration or assets. |
| DD-11 | Use a dependency-free Python contrast checker until the Node.js dashboard toolchain exists. | The environment has no Node.js and the repository has no dashboard package manifest. | Adding a package manager/toolchain solely to run one check. |

## Contrast adjustments

Contrast ratios are calculated using WCAG relative luminance from the supplied hex values. Locked source values are not silently changed. The provided palette has these notable outcomes:

| Pair | Ratio | Decision |
|---|---:|---|
| Obsidian `text-tertiary #70829E` on `surface-1 #0E1623` | 4.64:1 | Passes AA normal text; retain. |
| Obsidian `text-disabled #4A5A74` on `surface-1 #0E1623` | 2.60:1 | Fail for text; use only for nonessential disabled decoration. Required disabled labels use `text-secondary`. |
| Ivory `#6B7C95` on `#FFFFFF` | 4.25:1 | Fails AA normal text. Use locked tertiary for nonessential decoration only; required helper text uses Ivory secondary `#44556F`. |
| Ivory brand `#0B8CA0` on white | 3.98:1 | Passes 3:1 non-text UI target; fails normal text. Brand is for borders/fills; text on brand uses `#03181C` only after contrast check. |
| Ivory gold `#9A7424` on white | 4.29:1 | Fails normal text. Gold is an integrity icon/mark; adjacent text uses primary text. |
| High severity `#D9650F` on white | 3.61:1 | Passes non-text UI target; label uses `#0B1424`. |
| Medium severity `#B88A00` on white | 3.15:1 | Passes non-text UI target; label uses `#0B1424`. |

No values are altered in this baseline. Do not use any failing pair for normal-size text. Contrast of borders/icons is evaluated against the actual adjacent surface and is not inferred from a palette-only check.
