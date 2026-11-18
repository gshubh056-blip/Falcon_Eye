"""Check WCAG contrast for the FALCON design's declared semantic pairs."""

from __future__ import annotations

THEMES = {
    "obsidian": {
        "canvas": "#060A11",
        "base": "#0A101A",
        "surface1": "#0E1623",
        "surface2": "#131D2E",
        "surface3": "#192640",
        "primary": "#EAF0F8",
        "secondary": "#A3B3CB",
        "tertiary": "#70829E",
        "disabled": "#4A5A74",
        "cyan400": "#3CD7E8",
        "cyan500": "#1FC0D4",
        "cyan600": "#12A0B5",
        "brand": "#1FC0D4",
        "focus": "#3CD7E8",
        "onBrand": "#03181C",
        "gold300": "#E9CB86",
        "gold400": "#D9AE55",
        "gold500": "#C2963B",
        "critical": "#FF4D5E",
        "high": "#FF8A3D",
        "medium": "#F4C23E",
        "low": "#4DA3FF",
        "info": "#8FA1BD",
        "success": "#2FD08A",
        "offline": "#70829E",
        "syncing": "#3CD7E8",
        "warning": "#F4C23E",
    },
    "ivory": {
        "canvas": "#EEF2F7",
        "base": "#EEF2F7",
        "surface1": "#FFFFFF",
        "surface2": "#F6F8FB",
        "surface3": "#E8EEF6",
        "primary": "#0B1424",
        "secondary": "#44556F",
        "tertiary": "#6B7C95",
        "disabled": "#73829A",
        "brand": "#0B8CA0",
        "focus": "#0B8CA0",
        "onBrand": "#03181C",
        "gold": "#9A7424",
        "critical": "#D6293F",
        "high": "#D9650F",
        "medium": "#B88A00",
        "low": "#1F6FD1",
        "info": "#5B6E8B",
        "success": "#11875A",
        "offline": "#5B6E8B",
        "syncing": "#0B8CA0",
        "warning": "#B88A00",
    },
    "high-contrast": {
        "canvas": "#000000",
        "surface1": "#000000",
        "surface2": "#000000",
        "surface3": "#111111",
        "primary": "#FFFFFF",
        "secondary": "#FFFFFF",
        "tertiary": "#FFFFFF",
        "disabled": "#BDBDBD",
        "brand": "#00E5FF",
        "focus": "#00E5FF",
        "onBrand": "#000000",
        "critical": "#FF6B78",
        "high": "#FFB16E",
        "medium": "#FFE45E",
        "low": "#73B8FF",
        "info": "#D0D9E8",
        "success": "#55F0AC",
        "offline": "#D0D9E8",
        "syncing": "#00E5FF",
        "warning": "#FFE45E",
    },
    "night-dim": {
        "canvas": "#090B0E",
        "base": "#0D1014",
        "surface1": "#12171C",
        "surface2": "#171E24",
        "surface3": "#202A30",
        "primary": "#E8E3D8",
        "secondary": "#B8B4AA",
        "tertiary": "#9A9B91",
        "disabled": "#70756F",
        "brand": "#57B7BE",
        "focus": "#73D5DA",
        "onBrand": "#03181C",
        "gold300": "#E9CB86",
        "gold400": "#D9AE55",
        "gold500": "#C2963B",
        "critical": "#FF4D5E",
        "high": "#FF8A3D",
        "medium": "#F4C23E",
        "low": "#4DA3FF",
        "info": "#8FA1BD",
        "success": "#2FD08A",
        "offline": "#9A9B91",
        "syncing": "#73D5DA",
        "warning": "#F4C23E",
    },
}

# Text pairs are held to 4.5:1. Accents/severity indicators are UI boundaries
# and are held to 3:1. "tertiary" and "disabled" ivory text are intentionally
# excluded from text pairs and must only be used decoratively.
TEXT_PAIRS = (
    ("primary", "canvas"),
    ("primary", "surface1"),
    ("primary", "surface2"),
    ("secondary", "canvas"),
    ("secondary", "surface1"),
    ("secondary", "surface2"),
    ("onBrand", "brand"),
)
OPTIONAL_TEXT_PAIRS = (
    ("tertiary", "surface1"),
)
UI_PAIRS = (
    ("brand", "surface1"),
    ("focus", "surface1"),
    ("critical", "surface1"),
    ("high", "surface1"),
    ("medium", "surface1"),
    ("low", "surface1"),
    ("info", "surface1"),
    ("success", "surface1"),
    ("offline", "surface1"),
    ("syncing", "surface1"),
    ("warning", "surface1"),
    ("gold", "surface1"),
)


def luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (luminance(foreground), luminance(background)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def main() -> int:
    failed = False
    for theme_name, colors in THEMES.items():
        for foreground_key, background_key in TEXT_PAIRS:
            if foreground_key not in colors or background_key not in colors:
                continue
            value = ratio(colors[foreground_key], colors[background_key])
            passed = value >= 4.5
            failed |= not passed
            print(
                f"{theme_name}: {foreground_key}/{background_key} "
                f"{value:.2f}:1 {'PASS' if passed else 'FAIL (4.5:1)'}"
            )
        for foreground_key, background_key in OPTIONAL_TEXT_PAIRS:
            if foreground_key not in colors or background_key not in colors:
                continue
            value = ratio(colors[foreground_key], colors[background_key])
            if theme_name == "ivory":
                print(
                    f"{theme_name}: {foreground_key}/{background_key} "
                    f"{value:.2f}:1 DECORATIVE ONLY (use secondary for text)"
                )
                continue
            passed = value >= 4.5
            failed |= not passed
            print(
                f"{theme_name}: {foreground_key}/{background_key} "
                f"{value:.2f}:1 {'PASS' if passed else 'FAIL (4.5:1)'}"
            )
        for foreground_key, background_key in UI_PAIRS:
            if foreground_key not in colors or background_key not in colors:
                continue
            value = ratio(colors[foreground_key], colors[background_key])
            passed = value >= 3
            failed |= not passed
            print(
                f"{theme_name}: UI {foreground_key}/{background_key} "
                f"{value:.2f}:1 {'PASS' if passed else 'FAIL (3:1)'}"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
