from typing import List, Tuple
import threading

import pygame

import source.gui.assets as assets
from source import file
from source.logger import LoggerManager
from source.gui.constants import *  # pylint: disable=W0401,W0614  # noqa: F403
from source.gui.elements import BackgroundDrawer
from source.gui.helper import draw_text, draw_footer_button
from source.product_name import LONG_NAME
from source.smwc.entry import HackEntry


WINDOW_TITLE = LONG_NAME

# Header
DESCRIPTION_OFFSET = (16, 24)

# Footer
FOOTER_HEIGHT = 64

# Separator
SEPARATOR_OFFSET = 16  # x

# Selection
CURSOR_OFFSET = (SEPARATOR_OFFSET, 16)  # x, y
SELECTION_INDENT = 16

# Menu
MENU_HEIGHT = HEIGHT - HEADER_TOTAL - FOOTER_HEIGHT
MENU_ENTRY_HEIGHT = 96  # px

# Check box
CHECKBOX_OFFSET = 16  # y
CHECKBOX_DEMO_OFFSET = CURSOR_OFFSET[0] + 32  # x
CHECKBOX_FEATURED_OFFSET = CHECKBOX_DEMO_OFFSET + 48  # x

# Text
TEXT_OFFSET = CHECKBOX_FEATURED_OFFSET + 48  # x
NAME_OFFSET = 16  # y
AUTHOR_OFFSET = 8  # x
DIFFICULTY_OFFSET = NAME_OFFSET + 32  # y
DETAIL_OFFSET = DIFFICULTY_OFFSET + 24  # y

NO_HACKS_FOUND_MESSAGE = "No hacks found!"


# todo: arg for run after patched


def draw_checkbox(
    screen: pygame.Surface, state: bool, entry_y_pos: int, offset_x: int
) -> None:
    image = assets.CHECKBOX_ON_IMAGE if state else assets.CHECKBOX_OFF_IMAGE
    offset_y = entry_y_pos + CHECKBOX_OFFSET
    screen.blit(image, (offset_x, offset_y))


def draw_header(screen: pygame.Surface, hacks_found: bool):
    screen.blit(
        assets.LOGO_IMAGE,
        ((WIDTH - assets.LOGO_IMAGE.get_width()) // 2, LOGO_PADDING_Y),
    )

    if hacks_found:
        draw_text(
            screen,
            "Demo | Featured | Hack details",
            assets.FONT_MINOR,
            assets.COLOR_MINOR_NORMAL,
            (DESCRIPTION_OFFSET[0], HEADER_TOTAL - DESCRIPTION_OFFSET[1]),
        )


def draw_footer(screen: pygame.Surface):
    footer_y = (
        screen.get_height() - assets.BUTTON_B_IMAGE.get_height() - FOOTER_OFFSET[1]
    )
    apply_rect = draw_footer_button(
        screen,
        " Download and apply",
        assets.BUTTON_B_IMAGE,
        assets.KEY_RETURN_IMAGE,
        assets.FONT_MINOR,
        (FOOTER_OFFSET[0], footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    # todo: make y dependent on previous rect.top ... somehow
    filter_rect = draw_footer_button(
        screen,
        " Search with filter",
        assets.BUTTON_Y_IMAGE,
        assets.KEY_F_IMAGE,
        assets.FONT_MINOR,
        (apply_rect.right + FOOTER_BUTTONS_PADDING, footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    exit_rect = draw_footer_button(
        screen,
        " Exit",
        assets.BUTTON_START_IMAGE,
        assets.KEY_ESC_IMAGE,
        assets.FONT_MINOR,
        (filter_rect.right + FOOTER_BUTTONS_PADDING, footer_y),
        assets.COLOR_MINOR_NORMAL,
    )

    # logger
    footer_y = screen.get_height() - assets.FONT_LOG.get_height() - FOOTER_OFFSET[1]
    LoggerManager().handler.screen_logger.draw(
        screen,
        (screen.get_width() - FOOTER_OFFSET[0], footer_y),
        screen.get_width() - (exit_rect.right + FOOTER_BUTTONS_PADDING),
    )


def draw_hack_list(
    screen: pygame.Surface, selected_entry: int, scroll_offset: int, hack_list: list
):
    for i in range(
        scroll_offset,
        min(len(hack_list), scroll_offset + MENU_HEIGHT // MENU_ENTRY_HEIGHT),
    ):
        entry = hack_list[i]
        is_selected = i == selected_entry
        entry_y = HEADER_TOTAL + (i - scroll_offset) * MENU_ENTRY_HEIGHT
        indent = SELECTION_INDENT if is_selected else 0

        # name
        draw_text(
            screen,
            entry.name,
            assets.FONT_MAJOR,
            assets.COLOR_MAJOR_NORMAL
            if not is_selected
            else assets.COLOR_MAJOR_SELECTED,
            (TEXT_OFFSET + indent, entry_y + NAME_OFFSET),
        )

        # author
        name_text_width, _ = assets.FONT_MAJOR.size(entry.name)
        draw_text(
            screen,
            f"by {entry.author}",
            assets.FONT_MINOR,
            assets.COLOR_MAJOR_NORMAL
            if not is_selected
            else assets.COLOR_MAJOR_SELECTED,
            (
                name_text_width + TEXT_OFFSET + AUTHOR_OFFSET + indent,
                entry_y + NAME_OFFSET + 8,
            )
            # todo: replace 8 with actual calculated value, so title and line form one line
        )

        # difficulty
        draw_text(
            screen,
            entry.difficulty.value[0],
            assets.FONT_MINOR,
            assets.COLOR_MINOR_NORMAL
            if not is_selected
            else assets.COLOR_MINOR_SELECTED,
            (TEXT_OFFSET + indent, entry_y + DIFFICULTY_OFFSET),
        )

        # details
        draw_text(
            screen,
            (
                f"{str(entry.rating) + '/5.0' if entry.rating else 'No ratings given'} | "
                f"{entry.length} {'exit' if entry.length == 1 else 'exits'} | "
                f"{entry.download_count} downloads | {entry.date.strftime('%c')} | {entry.size}"
            ),
            assets.FONT_MINOR,
            assets.COLOR_MINOR_NORMAL
            if not is_selected
            else assets.COLOR_MINOR_SELECTED,
            (TEXT_OFFSET + indent, entry_y + DETAIL_OFFSET),
        )

        draw_checkbox(screen, entry.demo, entry_y, CHECKBOX_DEMO_OFFSET + indent)
        draw_checkbox(
            screen, entry.featured, entry_y, CHECKBOX_FEATURED_OFFSET + indent
        )

        # Render red triangle next to the selected entry
        if is_selected:
            draw_cursor(screen, entry_y, indent)

        # Draw a white separator line between entries
        draw_separator(screen, entry_y)


def draw_cursor(screen: pygame.Surface, entry_y: int, indent: int):
    cursor_offset_y = (
        entry_y + CURSOR_OFFSET[1] + (assets.CURSOR_IMAGE.get_height() // 2)
    )
    screen.blit(assets.CURSOR_IMAGE, (CURSOR_OFFSET[0] + indent, cursor_offset_y))


def draw_separator(screen: pygame.Surface, entry_y: int):
    separator_y = entry_y + MENU_ENTRY_HEIGHT
    pygame.draw.line(
        screen,
        assets.COLOR_SEPARATOR,
        (SEPARATOR_OFFSET, separator_y),
        (WIDTH - SEPARATOR_OFFSET, separator_y),
        1,
    )


def draw(
    screen: pygame.Surface,
    selected_entry: int,
    scroll_offset: int,
    hacks: list,
):
    hacks_found = len(hacks) > 0
    # Draw GUI
    draw_header(screen, hacks_found)
    draw_footer(screen)
    draw_hack_list(screen, selected_entry, scroll_offset, hacks)

    if not hacks_found:
        text_size = assets.FONT_MAJOR.size(NO_HACKS_FOUND_MESSAGE)
        draw_text(
            screen,
            NO_HACKS_FOUND_MESSAGE,
            assets.FONT_MAJOR,
            assets.COLOR_MAJOR_NORMAL,
            (
                (screen.get_width() - text_size[0]) // 2,
                (screen.get_height() - text_size[1]) // 2,
            ),
        )

    # Update the display
    pygame.display.flip()


def event_selection_up(selected_entry: int, scroll_offset: int) -> Tuple[int, int]:
    selected_entry = max(0, selected_entry - 1)
    if selected_entry < scroll_offset:
        scroll_offset = selected_entry
    return selected_entry, scroll_offset


def event_selection_down(
    selected_entry: int, scroll_offset: int, hack_list_len: int
) -> Tuple[int, int]:
    selected_entry = min(hack_list_len - 1, selected_entry + 1)
    if selected_entry >= scroll_offset + MENU_HEIGHT // MENU_ENTRY_HEIGHT:
        scroll_offset = min(
            hack_list_len - MENU_HEIGHT // MENU_ENTRY_HEIGHT,
            selected_entry - MENU_HEIGHT // MENU_ENTRY_HEIGHT + 1,
        )
    return selected_entry, scroll_offset


def event_select_entry(hack_list: list, selected_entry: int):
    LoggerManager().logger.info('Selected "%s"', hack_list[selected_entry].name)
    threading.Thread(
        target=file.download_and_run, args=(hack_list[selected_entry].download_url,)
    ).start()


def run(screen: pygame.Surface, hacks: List[HackEntry]) -> ScreenIntent:
    # Init window
    pygame.display.set_caption(LONG_NAME)
    background = BackgroundDrawer(screen, assets.BACKGROUND_IMAGE)

    # Main loop
    selected_entry = 0
    scroll_offset = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_entry, scroll_offset = event_selection_up(
                        selected_entry, scroll_offset
                    )
                elif event.key == pygame.K_DOWN:
                    selected_entry, scroll_offset = event_selection_down(
                        selected_entry, scroll_offset, len(hacks)
                    )
                elif event.key == pygame.K_RETURN:
                    event_select_entry(hacks, selected_entry)
                elif event.key == pygame.K_ESCAPE:
                    return ScreenIntent.EXIT
                elif event.key == pygame.K_f:
                    return ScreenIntent.FILTER

            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:  # D-pad up
                    selected_entry, scroll_offset = event_selection_up(
                        selected_entry, scroll_offset
                    )
                elif event.value[1] == -1:  # D-pad down
                    selected_entry, scroll_offset = event_selection_down(
                        selected_entry, scroll_offset, len(hacks)
                    )

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button on the gamepad
                    event_select_entry(hacks, selected_entry)
                elif event.button == 7:  # Start button on the gamepad
                    return ScreenIntent.EXIT

        background.draw()
        draw(screen, selected_entry, scroll_offset, hacks)
