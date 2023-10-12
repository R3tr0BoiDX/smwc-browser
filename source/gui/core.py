import pygame

from source.gui import assets
from source.gui.constants import HEIGHT, WIDTH
from source.gui.screens import filter as filter_screen
from source.gui.screens import browser as browser_screen
from source.gui.constants import ScreenIntent
from source.smwc.crawler import get_hacks

# Initialize Pygame
pygame.init()

# Initialize gamepad
pygame.joystick.init()
_ = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Set window icon
pygame.display.set_icon(assets.ICON_IMAGE)

# todo: universally use helper.draw_text()


def run():
    # WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # todo: arg

    hacks = get_hacks()
    running = True
    intent = ScreenIntent.FILTER  # start with browser

    while running:
        if intent == ScreenIntent.BROWSER:
            intent = browser_screen.run(screen, hacks)

        if intent == ScreenIntent.FILTER:
            result = filter_screen.run(screen)

            if isinstance(result, tuple):
                intent, hacks = result
            else:
                intent = result

        if intent == ScreenIntent.EXIT:
            running = False

    pygame.quit()
