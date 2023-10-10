import pygame

import source.gui.scenes.filter as filter_screen
from source.gui.constants import WIDTH, HEIGHT

# Initialize Pygame
pygame.init()


def run():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        running = filter_screen.run(screen)

    pygame.quit()
