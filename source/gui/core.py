import pygame

from source.arguments import Arguments
from source.gui import assets
from source.gui.constants import ScreenIntent, get_screen_size
from source.gui.screens import browser as browser_screen
from source.gui.screens import filter as filter_screen
from source.smwc.crawler import get_page

# Initialize Pygame
pygame.init()

# Initialize gamepad
pygame.joystick.init()
_ = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Set window icon
pygame.display.set_icon(assets.ICON_IMAGE)


def run():
    """Run the GUI."""

    # Initialize screen
    if Arguments().get_fullscreen():
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode(get_screen_size())

    page = get_page()
    running = True
    intent = ScreenIntent.BROWSER  # start with browser

    while running:
        if intent == ScreenIntent.BROWSER:
            intent = browser_screen.run(screen, page)

        if intent == ScreenIntent.FILTER:
            result = filter_screen.run(screen)

            if isinstance(result, tuple):
                intent, page = result
            else:
                intent = result

        if intent == ScreenIntent.EXIT:
            running = False

    pygame.quit()
