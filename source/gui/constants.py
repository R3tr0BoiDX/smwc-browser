from enum import Enum

import pygame

from source.arguments import Arguments

# Minimal screen dimensions
WIDTH, HEIGHT = 1280, 800
if Arguments().get_fullscreen():  # todo: not a big fan of this solution
    pygame.display.init()
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Header
LOGO_HEIGHT = 96
HEADER_OFFSET = (32, 32)
HEADER_TOTAL = LOGO_HEIGHT + (2 * HEADER_OFFSET[1])

# Footer
FOOTER_OFFSET = (24, 24)
FOOTER_BUTTONS_PADDING = 32


class ScreenIntent(Enum):
    """Enum for screen intents."""

    EXIT = 0
    BROWSER = 1
    FILTER = 2
