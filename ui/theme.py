"""
ui/theme.py
Central style constants so every UI component pulls from the same
palette/fonts — matching the dark navy + glowing blue look of the
Marcus splash art.
"""

# --- Colors ---
BG_DARK = "#0A0E17"          # near-black navy background
BG_PANEL = "#0F1624"         # slightly lighter panel background
BG_SIDEBAR = "#0B1120"       # sidebar background
BORDER_GLOW = "#1E3A5F"      # subtle border on panels

ACCENT_BLUE = "#2FA8FF"      # primary glow blue (buttons, active nav)
ACCENT_BLUE_DIM = "#1B6FB8"  # hover/pressed state
ACCENT_CYAN = "#5FD4FF"      # secondary highlight (headings, icons)

TEXT_PRIMARY = "#F2F6FB"     # near-white body text
TEXT_SECONDARY = "#8FA3BF"   # muted secondary text
TEXT_DISABLED = "#4A5A70"

BUBBLE_MARCUS_BG = "#132038"     # Marcus's response bubble
BUBBLE_USER_BG = "#1B2C4A"       # user's recognized-speech bubble
STATUS_LISTENING = "#2FA8FF"     # mic active glow
STATUS_IDLE = "#3A4A63"          # mic idle
STATUS_THINKING = "#5FD4FF"

# --- Fonts ---
FONT_FAMILY = "Segoe UI"          # ships with Windows, clean/modern
FONT_FAMILY_MONO = "Consolas"

FONT_TITLE = (FONT_FAMILY, 28, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 14)
FONT_NAV = (FONT_FAMILY, 14)
FONT_BODY = (FONT_FAMILY, 13)
FONT_BUBBLE_SENDER = (FONT_FAMILY, 11, "bold")
FONT_BUBBLE_TEXT = (FONT_FAMILY, 13)
FONT_STATUS = (FONT_FAMILY, 11)

# --- Layout ---
SIDEBAR_WIDTH = 200
CORNER_RADIUS = 12
WINDOW_MIN_SIZE = (960, 620)
