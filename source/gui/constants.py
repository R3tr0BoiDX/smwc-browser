from enum import Enum

# Minimal screen dimensions
WIDTH, HEIGHT = 1280, 720

# Header
LOGO_HEIGHT = 96
LOGO_PADDING_Y = 32
HEADER_TOTAL = LOGO_HEIGHT + (2 * LOGO_PADDING_Y)

# Footer
FOOTER_OFFSET = (24, 24)
FOOTER_BUTTONS_PADDING = 32


class ScreenIntent(Enum):
    """Enum for screen intents."""

    EXIT = 0
    BROWSER = 1
    FILTER = 2
