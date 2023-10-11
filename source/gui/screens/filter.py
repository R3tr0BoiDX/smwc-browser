from typing import Union, Tuple

import pygame

from source.gui import assets
from source.gui.constants import *  # pylint: disable=W0401,W0614  # noqa: F403
from source.gui.elements import BackgroundDrawer, CarouselSelect, Checkbox, Textfield
from source.gui.elements.gui_element import GUIElement
from source.gui.helper import draw_footer_button
from source.product_name import LONG_NAME
from source.smwc.entry import get_difficulty_names, index_to_difficulty
from source.smwc.crawler import get_hacks

WINDOW_TITLE = LONG_NAME + ": Filter"

# Menu
ENTRIES_PADDING = 8


def draw_header(screen: pygame.Surface):
    screen.blit(
        assets.LOGO_IMAGE,
        ((screen.get_width() - assets.LOGO_IMAGE.get_width()) // 2, LOGO_PADDING_Y),
    )


def draw_footer(screen: pygame.Surface, space: bool):
    footer_y = (
        screen.get_height() - assets.BUTTON_B_IMAGE.get_height() - FOOTER_OFFSET[1]
    )
    back_rect = draw_footer_button(
        screen,
        " Back",
        assets.BUTTON_A_IMAGE,
        assets.KEY_ESC_IMAGE,
        assets.FONT_MINOR,
        (FOOTER_OFFSET[0], footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    # todo: make y dependent on previous rect.top ... somehow
    apply_rect = draw_footer_button(
        screen,
        " Apply filter",
        assets.BUTTON_Y_IMAGE,
        assets.KEY_RETURN_IMAGE,
        assets.FONT_MINOR,
        (back_rect.right + FOOTER_BUTTONS_PADDING, footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    clear_react = draw_footer_button(
        screen,
        " Clear filter",
        assets.BUTTON_X_IMAGE,
        assets.KEY_BACKSPACE_IMAGE,
        assets.FONT_MINOR,
        (apply_rect.right + FOOTER_BUTTONS_PADDING, footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    if space:
        draw_footer_button(
            screen,
            " Toggle",
            assets.BUTTON_B_IMAGE,
            assets.KEY_SPACE_IMAGE,
            assets.FONT_MINOR,
            (clear_react.right + FOOTER_BUTTONS_PADDING, footer_y),
            assets.COLOR_MINOR_NORMAL,
        )


def run(screen: pygame.Surface) -> Union[Tuple[ScreenIntent, list], ScreenIntent]:
    pygame.display.set_caption(WINDOW_TITLE)
    background = BackgroundDrawer(screen, assets.BACKGROUND_IMAGE)

    # todo: carousel for sort by
    menu = [
        Textfield(screen, "Name:", "Words given in the name of hack"),
        Textfield(screen, "Authors:", "Creator of hack, up to 5, comma separated"),
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
    space = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ScreenIntent.EXIT

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_TAB]:
                    selected_option = (selected_option + 1) % len(menu)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu)
                elif event.key == pygame.K_RETURN:
                    authors = menu[1].get_value()
                    authors = authors.split(",") if authors else None
                    authors = (
                        [author.strip() for author in authors]
                        if isinstance(authors, list)
                        else None
                    )

                    tags = menu[2].get_value()
                    tags = tags.split(",") if tags else None
                    tags = (
                        [tag.strip() for tag in tags]
                        if isinstance(tags, list)
                        else None
                    )

                    difficulty = index_to_difficulty(menu[5].get_value())

                    hacks = get_hacks(
                        name=menu[0].get_value(),
                        authors=authors,
                        tags=tags,
                        demo=menu[3].get_value(),
                        featured=menu[4].get_value(),
                        difficulty=difficulty,
                        description=menu[6].get_value(),
                    )

                    return ScreenIntent.BROWSER, hacks

                elif event.key == pygame.K_ESCAPE:
                    return ScreenIntent.BROWSER

            menu[selected_option].active(event)
            space = isinstance(menu[selected_option], Checkbox)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
            for element in menu:
                if isinstance(element, GUIElement):
                    element.clear_value()

        # Draw other
        background.draw()
        draw_header(screen)
        draw_footer(screen, space)

        # Draw elements
        element_x = screen.get_width() // 2
        element_y = HEADER_TOTAL
        for i, element in enumerate(menu):
            if isinstance(element, GUIElement):
                element_rect = element.draw(
                    (element_x, element_y),
                    i == selected_option,
                )
                element_y = element_rect.bottom + ENTRIES_PADDING

        pygame.display.flip()
    return ScreenIntent.EXIT  # pragma: no cover, mypy wants it
