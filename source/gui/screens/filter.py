from typing import Union, Tuple, List

import pygame

from source.gui import assets
from source.gui.constants import *  # pylint: disable=W0401,W0614  # noqa: F403
from source.gui.elements import (
    BackgroundDrawer,
    CarouselSelect,
    Textfield,
    RadioButton,
    Checkbox,
)
from source.gui.elements.gui_element import GUIElement
from source.gui.helper import draw_footer_button
from source.product_name import LONG_NAME
from source.smwc.entry import (
    HackEntry,
    get_difficulty_names,
    index_to_difficulty,
    get_sort_by_names,
    index_to_sort_by,
)
from source.smwc.crawler import get_hacks

WINDOW_TITLE = LONG_NAME + ": Search with filters"

# Menu
ENTRIES_PADDING = 8
TRANSLATE_RADIO_BUTTON = {"Any": None, "Yes": True, "No": False}


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
        ": Back",
        assets.BUTTON_B_IMAGE,
        assets.KEY_ESC_IMAGE,
        assets.FONT_MINOR,
        (FOOTER_OFFSET[0], footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    # todo: make y dependent on previous rect.top ... somehow
    apply_rect = draw_footer_button(
        screen,
        ": Apply filter",
        assets.BUTTON_Y_IMAGE,
        assets.KEY_RETURN_IMAGE,
        assets.FONT_MINOR,
        (back_rect.right + FOOTER_BUTTONS_PADDING, footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    clear_react = draw_footer_button(
        screen,
        ": Clear filter",
        assets.BUTTON_X_IMAGE,
        [assets.KEY_CTRL_IMAGE, assets.KEY_BACKSPACE_IMAGE],
        assets.FONT_MINOR,
        (apply_rect.right + FOOTER_BUTTONS_PADDING, footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    if space:
        draw_footer_button(
            screen,
            ": Toggle",
            assets.BUTTON_A_IMAGE,
            assets.KEY_SPACE_IMAGE,
            assets.FONT_MINOR,
            (clear_react.right + FOOTER_BUTTONS_PADDING, footer_y),
            assets.COLOR_MINOR_NORMAL,
        )


def search_hacks(menu: List[GUIElement]) -> List[HackEntry]:
    authors = menu[1].get_value()
    authors = authors.split(",") if authors else None
    authors = (
        [author.strip() for author in authors] if isinstance(authors, list) else None
    )

    tags = menu[2].get_value()
    tags = tags.split(",") if tags else None
    tags = [tag.strip() for tag in tags] if isinstance(tags, list) else None

    difficulty = index_to_difficulty(menu[5].get_value())
    items = list(TRANSLATE_RADIO_BUTTON.items())
    demo = items[menu[3].get_value()][1]
    featured = items[menu[4].get_value()][1]
    sort_by = index_to_sort_by(menu[7].get_value())

    return get_hacks(
        name=menu[0].get_value(),
        authors=authors,
        tags=tags,
        demo=demo,
        featured=featured,
        difficulty=difficulty,
        description=menu[6].get_value(),
        sort_by=sort_by,
        ascending=menu[8].get_value(),
    )


def clear_filter(menu: List[GUIElement]):
    for element in menu:
        if isinstance(element, GUIElement):
            element.clear_value()


def run(screen: pygame.Surface) -> Union[Tuple[ScreenIntent, list], ScreenIntent]:
    pygame.display.set_caption(WINDOW_TITLE)
    background = BackgroundDrawer(screen, assets.BACKGROUND_IMAGE)

    menu = [
        Textfield(screen, "Name:", "Words given in the name of hack"),
        Textfield(screen, "Authors:", "Creator of hack, up to 5, comma separated"),
        Textfield(screen, "Tags:", "Labeling keywords, up to 5, comma separated"),
        RadioButton(
            screen,
            "Demo:",
            "Hacks can be demos or need to be full length",
            list(TRANSLATE_RADIO_BUTTON.keys()),
        ),
        RadioButton(
            screen,
            "Featured:",
            "If the hack was featured before",
            list(TRANSLATE_RADIO_BUTTON.keys()),
        ),
        CarouselSelect(
            screen, "Type:", "Difficulty of the hack", get_difficulty_names()
        ),
        Textfield(screen, "Description:", "Words given in the description"),
        CarouselSelect(
            screen, "Sort by:", "Attribute to sort results by", get_sort_by_names()
        ),
        Checkbox(screen, "Ascending:", "Sort results in ascending order"),
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
                elif event.key in [pygame.K_RETURN, pygame.KSCAN_RETURN]:
                    return ScreenIntent.BROWSER, search_hacks(menu)
                elif event.key == pygame.K_ESCAPE:
                    return ScreenIntent.BROWSER

            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == -1:  # D-pad down
                    selected_option = (selected_option + 1) % len(menu)
                elif event.value[1] == 1:  # D-pad up
                    selected_option = (selected_option - 1) % len(menu)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:  # B button on the gamepad
                    return ScreenIntent.BROWSER
                elif event.button == 2:  # X button on the gamepad
                    clear_filter(menu)
                elif event.button == 3:  # Y button on the gamepad
                    return ScreenIntent.BROWSER, search_hacks(menu)

            menu[selected_option].active(event)
            space = isinstance(menu[selected_option], Checkbox)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
            clear_filter(menu)

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
