import pygame

import source.gui.assets as assets
from source.gui.elements import BackgroundDrawer, CarouselSelect, Checkbox, Textfield
from source.gui.elements.gui_element import GUIElement
from source.smwc.entry import get_difficulty_names
from source.product_name import LONG_NAME

WINDOW_TITLE = LONG_NAME + ": Filter"

# Header
LOGO_HEIGHT = 96
LOGO_PADDING_Y = 32
HEADER_TOTAL = LOGO_HEIGHT + (2 * LOGO_PADDING_Y)

# Menu
ENTRIES_OFFFSET = 16
MENU_ENTRY_HEIGHT = 64


def draw_header(screen: pygame.Surface):
    screen.blit(
        assets.LOGO_IMAGE,
        ((screen.get_width() - assets.LOGO_IMAGE.get_width()) // 2, LOGO_PADDING_Y),
    )


def run(screen: pygame.Surface) -> bool:
    pygame.display.set_caption(WINDOW_TITLE)
    background = BackgroundDrawer(screen, assets.BACKGROUND_IMAGE)

    menu = [
        Textfield(screen, "Name:", "Words given in the name of hack"),
        Textfield(screen, "Author:", "Creator of hack, up to 5, comma separated"),
        Textfield(screen, "Tags:", "Labeling keywords, up to 5, comma separated"),
        Checkbox(screen, "Demo:", "Hacks can be demos or need to be full length"),
        Checkbox(screen, "Featured:", "If the hack was featured before"),
        CarouselSelect(
            screen, "Type:", "Difficulty of the hack", get_difficulty_names()
        ),
        Textfield(screen, "Description:", "Words given in the description"),
    ]

    selected_option = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu)
                # elif:
                #   if submit button, return True

            menu[selected_option].active(event)

        # Draw
        background.draw()
        draw_header(screen)

        # Draw elements
        for i, element in enumerate(menu):
            if isinstance(element, GUIElement):
                element.draw(
                    (screen.get_width() // 2, HEADER_TOTAL + (MENU_ENTRY_HEIGHT * i)),
                    i == selected_option,
                )
        pygame.display.flip()
