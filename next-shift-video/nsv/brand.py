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
