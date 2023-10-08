import pygame

from source.gui.core import WHITE
# from source.gui.elements.checkbox import Checkbox
from source.gui.elements.textfield import Textfield

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Filter")

# Checkbox properties
label_font = pygame.font.Font(None, 48)

# Font setup
font = pygame.font.Font(None, 36)

# checkbox = Checkbox(screen, (100, 100), "enable: ", font)
textbox = Textfield(screen, (32, 200), "input text: ", font)

# Main loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checkbox.active(event)
        textbox.active(event)

    # draw
    screen.fill(WHITE)
    # checkbox.draw()
    textbox.draw()

    pygame.display.flip()

pygame.quit()
