import pygame

from source.gui import assets
from source.gui.constants import HEIGHT, WIDTH
from source.gui.screens import filter as filter_screen
from source.gui.screens import browser as browser_screen

# Initialize Pygame
pygame.init()

# Initialize gamepad
pygame.joystick.init()
_ = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Set window icon
pygame.display.set_icon(assets.ICON_IMAGE)


def run():
    # WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # todo: arg

    running = True
    while running:
        running = browser_screen.run(screen)

    pygame.quit()
