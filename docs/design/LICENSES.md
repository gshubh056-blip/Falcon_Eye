# Design Asset and Library Licenses

No third-party font or icon package has been added to the workspace yet. The table distinguishes installed libraries from candidates. Before distributing an asset, preserve its license text and verify the exact package/version license.

| Asset/library | Proposed use | License | Offline rule / status |
|---|---|---|---|
| Sora | Headings and wordmark | SIL Open Font License 1.1 | Self-host WOFF2; not installed |
| Geist Sans | UI text | SIL Open Font License 1.1 | Self-host WOFF2; not installed |
| Geist Mono | Hashes, IDs and data | SIL Open Font License 1.1 | Self-host WOFF2; not installed |
| Noto Sans Devanagari | Hindi UI | SIL Open Font License 1.1 | Self-host WOFF2; not installed |
| Lucide | General UI icons | ISC | Bundle local package; not installed |
| Radix UI primitives | Accessible interaction behavior | MIT | Bundle locally; not installed |
| React / React DOM | UI framework (TRD: React 18) | MIT | Bundle locally; no dashboard package present |
| Tailwind CSS | Utility generation, if adopted | MIT | Build-time only; no dashboard package present |
| Motion for React | Optional motion primitives | MIT | Bundle locally; use sparingly; not installed |
| ECharts | Optional charts | Apache-2.0 | Bundle locally; no runtime network dependency |
| MapLibre GL JS | Optional offline map rendering | BSD-3-Clause | Bundle locally; tiles/styles must be local |
| opencv-python-headless 4.10.0.84 | Camera/video frame capture | Apache-2.0 | Installed; package metadata verified; device support is recorded separately |

Falcon marks, terrain contours, radar motifs and empty-state art are original SVGs authored for this project; they contain no third-party imagery. Do not use stock photos or real-person imagery. Do not include an emoji as a substitute for an icon.

## Required license verification

1. Resolve exact package versions in the dashboard manifest.
2. Verify each package's license from its published package metadata and repository license file.
3. Include required attribution/license texts in the shipped distribution.
4. Record version and evidence in this table before release.
5. Confirm offline startup with external network access blocked.
