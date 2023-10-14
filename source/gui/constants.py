from enum import Enum
from typing import Tuple

import pygame

from source.arguments import Arguments

# Minimal screen dimensions
WIDTH, HEIGHT = 1280, 800


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


def get_width() -> int:
    """Get the screen width, taking into account fullscreen mode.

    Returns:
        int: The screen width.
    """
    width = WIDTH
    if Arguments().get_fullscreen():
        if not pygame.display.get_init():
            pygame.display.init()
        width = pygame.display.Info().current_w

    return width


def get_height() -> int:
    """Get the screen height, taking into account fullscreen mode.

    Returns:
        int: The screen height.
    """
    height = HEIGHT
    if Arguments().get_fullscreen():
        if not pygame.display.get_init():
            pygame.display.init()
        height = pygame.display.Info().current_h

    return height


def get_screen_size() -> Tuple[int, int]:
    """Get the screen size, taking into account fullscreen mode.

    Returns:
        tuple: The screen size.
    """
    return (get_width(), get_height())
