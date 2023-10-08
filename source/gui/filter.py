import pygame

import source.gui.assets as assets
from source.gui.core import GUIElement
from source.gui.elements import BackgroundDrawer, CarouselSelect, Checkbox, Textfield
from source.smwc.entry import get_difficulty_names

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
# WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Font
FONT_TITLE = pygame.font.Font(assets.FONT_TYPEFACE, assets.FONT_SIZE_TITLE)

# Header
LOGO_HEIGHT = 96
LOGO_PADDING_Y = 16
HEADER_TOTAL = LOGO_HEIGHT + (2 * LOGO_PADDING_Y)

# Menu
ENTRIES_OFFFSET = 16
MENU_ENTRY_HEIGHT = 48  # px

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Filter")

background = BackgroundDrawer(screen, assets.BACKGROUND_IMAGE)

menu = [
    Textfield(screen, "Name: ", FONT_TITLE),
    Textfield(screen, "Author: ", FONT_TITLE),
    Textfield(screen, "Tags: ", FONT_TITLE),
    Checkbox(screen, "Demo: ", FONT_TITLE),
    Checkbox(screen, "Featured: ", FONT_TITLE),
    CarouselSelect(screen, "Type: ", FONT_TITLE, get_difficulty_names()),
    Textfield(screen, "Description: ", FONT_TITLE),
]


def draw_header(screen: pygame.Surface):
    screen.blit(
        assets.LOGO_IMAGE,
        ((WIDTH - assets.LOGO_IMAGE.get_width()) // 2, LOGO_PADDING_Y),
    )


# Main loop
selected_option = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu)
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu)

            menu[selected_option].active(event)

    # draw
    screen.fill(assets.BG_COLOR)
    background.draw()
    draw_header(screen)

    for i, element in enumerate(menu):
        if isinstance(element, GUIElement):
            element.draw((WIDTH//4, HEADER_TOTAL + (MENU_ENTRY_HEIGHT * i)), i == selected_option)

    pygame.display.flip()

pygame.quit()
