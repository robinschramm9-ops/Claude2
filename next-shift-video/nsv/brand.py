"""THE NEXT SHIFT brand system: one place for every visual constant.

Change the look of every future video by editing this file only.
"""

CHANNEL = "THE NEXT SHIFT"
TAGLINE = "Understand tomorrow before it happens."

W, H = 1920, 1080
FPS = 30

# Palette ---------------------------------------------------------------
BG = "#0B0C0F"          # near-black charcoal
BG_2 = "#14161C"        # raised surface
GRID = "#1C1F27"        # background grid lines
INK = "#F4F5F7"         # primary text
INK_2 = "#9AA0AD"       # secondary text
INK_3 = "#5C6270"       # tertiary / captions
ACCENT = "#3D8BFF"      # electric blue: the "subject" of each scene
ACCENT_2 = "#B6F23A"    # lime: positive change / winner / highlight
WARN = "#FF5A4E"        # loser / risk / decline (use sparingly)

# Fonts (cairosvg ignores numeric weights, so weights are family names) --
F_LIGHT = "Inter Light"
F_REG = "Inter"
F_MED = "Inter Medium"
F_SEMI = "Inter SemiBold"
F_BOLD = "Inter ExtraBold"
F_MONO = "DejaVu Sans Mono"

FONT_FILES = {  # used for text measurement (wrapping, overflow QC)
    F_LIGHT: "Inter-Light.otf",
    F_REG: "Inter-Regular.otf",
    F_MED: "Inter-Medium.otf",
    F_SEMI: "Inter-SemiBold.otf",
    F_BOLD: "Inter-ExtraBold.otf",
}
FONT_DIRS = ["/usr/share/fonts/opentype/inter", "/usr/share/fonts/truetype/inter",
             "/Library/Fonts", "~/Library/Fonts", "~/.fonts", "~/.local/share/fonts",
             "C:/Windows/Fonts"]

# Layout ----------------------------------------------------------------
SAFE_X = 160            # title-safe margins
SAFE_Y = 110
MIN_TEXT_PX = 28        # QC: nothing smaller is allowed on a 1080p frame

# Motion ----------------------------------------------------------------
SCENE_FADE = 0.35       # seconds of fade in/out on every scene
CAMERA_PUSH = 0.035     # slow push-in per scene (3.5% scale) so no frame is static
SCENE_PAD = 0.45        # silence after each narration block (breathing room)

# Themes ------------------------------------------------------------------
# A storyboard picks one with "theme": "dark" (default) or "white".
CARD_RADIUS = 12        # corner radius of cards/boxes
SOFT = False            # soft-shadow cards instead of outlined ones
BG_BLOBS = False        # soft background shapes instead of the grid
THEME = "dark"

FONT_FILES.update({
    "Quicksand Light": "Quicksand-Light.ttf", "Quicksand": "Quicksand-Regular.ttf",
    "Quicksand Medium": "Quicksand-Medium.ttf", "Quicksand Bold": "Quicksand-Bold.ttf",
})
FONT_DIRS.insert(0, "/usr/share/fonts/truetype/quicksand")

_DARK = dict(BG=BG, BG_2=BG_2, GRID=GRID, INK=INK, INK_2=INK_2, INK_3=INK_3, ACCENT=ACCENT, ACCENT_2=ACCENT_2,
             WARN=WARN, F_LIGHT=F_LIGHT, F_REG=F_REG, F_MED=F_MED, F_SEMI=F_SEMI, F_BOLD=F_BOLD,
             CARD_RADIUS=12, SOFT=False, BG_BLOBS=False, CHANNEL=CHANNEL)
THEMES = {
    "dark": _DARK,
    # White, simple, extremely round, natural (approved style frames, Nov 2026)
    "white": dict(BG="#F7F6F2", BG_2="#FFFFFF", GRID="#E7E4DD", INK="#2E2F2C", INK_2="#6F6C66", INK_3="#9A978F",
                  ACCENT="#7FAF3E", ACCENT_2="#9CCB5A", WARN="#D9826B",
                  F_LIGHT="Quicksand Light", F_REG="Quicksand Medium", F_MED="Quicksand Medium",
                  F_SEMI="Quicksand Bold", F_BOLD="Quicksand Bold",
                  CARD_RADIUS=48, SOFT=True, BG_BLOBS=True, CHANNEL="the next shift"),
}


def apply_theme(name: str | None):
    """Switch every brand constant to a theme. Call before rendering (each worker process calls it too)."""
    global THEME
    name = name or "dark"
    if name not in THEMES:
        raise SystemExit(f"unknown theme '{name}' (available: {', '.join(THEMES)})")
    globals().update(THEMES[name])
    THEME = name
