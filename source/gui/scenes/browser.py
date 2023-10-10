import sys
import logging

import pygame

from source.smwc import crawler
from source import file
from source.product_name import LONG_NAME
from source.gui.elements import BackgroundDrawer
import source.gui.assets as assets
from source.gui.helper import draw_text

pygame.init()

WIDTH, HEIGHT = 1280, 720
# WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Font
FONT_TITLE = pygame.font.Font(assets.FONT_TYPEFACE, assets.FONT_SIZE_TITLE)
FONT_DETAILS = pygame.font.Font(assets.FONT_TYPEFACE, assets.FONT_SIZE_DETAIL)

# Header
LOGO_HEIGHT = 96
LOGO_PADDING_Y = 16
HEADER_TOTAL = LOGO_HEIGHT + (2 * LOGO_PADDING_Y)
DESCRIPTION_OFFSET = (16, 24)

# Footer
FOOTER_HEIGHT = 48
FOOTER_OFFSET = (24, 56)

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

logger = logging.getLogger(__name__)


def draw_checkbox(
    screen: pygame.Surface, state: bool, entry_y_pos: int, offset_x: int
) -> None:
    image = assets.CHECKBOX_ON_IMAGE if state else assets.CHECKBOX_OFF_IMAGE
    offset_y = entry_y_pos + CHECKBOX_OFFSET
    screen.blit(image, (offset_x, offset_y))


# Main loop
def draw_header(screen: pygame.Surface):
    screen.blit(
        assets.LOGO_IMAGE,
        ((WIDTH - assets.LOGO_IMAGE.get_width()) // 2, LOGO_PADDING_Y),
    )
    draw_text(
        screen,
        "Demo | Featured | Hack details",
        FONT_DETAILS,
        assets.DETAIL_NORMAL,
        (DESCRIPTION_OFFSET[0], HEADER_TOTAL - DESCRIPTION_OFFSET[1]),
    )


def draw_footer(screen: pygame.Surface):
    # todo: idea: create logger, that sets the bottom text in footer

    footer_y = HEIGHT - assets.BUTTON_Y_IMAGE.get_width() - FOOTER_OFFSET[1]
    screen.blit(assets.BUTTON_Y_IMAGE, (FOOTER_OFFSET[0], footer_y))

    slash_x = FOOTER_OFFSET[0] + assets.BUTTON_Y_IMAGE.get_width()
    draw_text(
        screen, "/", FONT_DETAILS, assets.DETAIL_NORMAL, (slash_x, footer_y)
    )

    f_key_x = slash_x + FONT_DETAILS.size("/")[0]
    screen.blit(assets.KEY_F_IMAGE, (f_key_x, footer_y))

    filter_text_x = f_key_x + assets.KEY_F_IMAGE.get_width()
    draw_text(
        screen,
        ": Apply filter",
        FONT_DETAILS,
        assets.DETAIL_NORMAL,
        (filter_text_x, footer_y),
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
            FONT_TITLE,
            assets.ENTRY_NORMAL if not is_selected else assets.ENTRY_SELECTED,
            (TEXT_OFFSET + indent, entry_y + NAME_OFFSET),
        )

        # author
        name_text_width, _ = FONT_TITLE.size(entry.name)
        draw_text(
            screen,
            f"by {entry.author}",
            FONT_DETAILS,
            assets.ENTRY_NORMAL if not is_selected else assets.ENTRY_SELECTED,
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
            FONT_DETAILS,
            assets.DETAIL_NORMAL if not is_selected else assets.DETAIL_SELECTED,
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
            FONT_DETAILS,
            assets.DETAIL_NORMAL if not is_selected else assets.DETAIL_SELECTED,
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
    cursor_offset_y = entry_y + CURSOR_OFFSET[1] + (CURSOR_IMAGE.get_height() // 2)
    screen.blit(CURSOR_IMAGE, (CURSOR_OFFSET[0] + indent, cursor_offset_y))


def draw_separator(screen: pygame.Surface, entry_y: int):
    separator_y = entry_y + MENU_ENTRY_HEIGHT
    pygame.draw.line(
        screen,
        assets.SEPARATOR_COLOR,
        (SEPARATOR_OFFSET, separator_y),
        (WIDTH - SEPARATOR_OFFSET, separator_y),
        1,
    )


def draw(
    screen: pygame.Surface,
    selected_entry: int,
    scroll_offset: int,
    hack_list: list,
):

    # Draw GUI
    draw_header(screen)
    # draw_footer(screen)  # todo: enable again once filter screen is build
    draw_hack_list(screen, selected_entry, scroll_offset, hack_list)

    # Update the display
    pygame.display.flip()


def handle_events(selected_entry: int, scroll_offset: int, hack_list: list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, selected_entry, scroll_offset
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_entry, scroll_offset = event_selection_up(
                    selected_entry, scroll_offset
                )
            elif event.key == pygame.K_DOWN:
                selected_entry, scroll_offset = event_selection_down(
                    selected_entry, scroll_offset, len(hack_list)
                )
            elif event.key == pygame.K_RETURN:
                event_select_entry(hack_list, selected_entry)
            elif event.key == pygame.K_ESCAPE:
                return False, selected_entry, scroll_offset

        elif event.type == pygame.JOYHATMOTION:
            if event.value[1] == 1:  # D-pad up
                selected_entry, scroll_offset = event_selection_up(
                    selected_entry, scroll_offset
                )
            elif event.value[1] == -1:  # D-pad down
                selected_entry, scroll_offset = event_selection_down(
                    selected_entry, scroll_offset, len(hack_list)
                )

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # A button on the gamepad
                event_select_entry(hack_list, selected_entry)
            elif event.button == 7:  # Start button on the gamepad
                return False, selected_entry, scroll_offset

    return True, selected_entry, scroll_offset


def event_selection_up(selected_entry: int, scroll_offset: int) -> int:
    selected_entry = max(0, selected_entry - 1)
    if selected_entry < scroll_offset:
        scroll_offset = selected_entry
    return selected_entry, scroll_offset


def event_selection_down(
    selected_entry: int, scroll_offset: int, hack_list_len: int
) -> int:
    selected_entry = min(hack_list_len - 1, selected_entry + 1)
    if selected_entry >= scroll_offset + MENU_HEIGHT // MENU_ENTRY_HEIGHT:
        scroll_offset = min(
            hack_list_len - MENU_HEIGHT // MENU_ENTRY_HEIGHT,
            selected_entry - MENU_HEIGHT // MENU_ENTRY_HEIGHT + 1,
        )
    return selected_entry, scroll_offset


def event_select_entry(hack_list: list, selected_entry: int):
    logger.info("Selected: %s", hack_list[selected_entry].name)
    file.download_and_run(hack_list[selected_entry].download_url)


def run():
    # Initialize screen
    pygame.display.set_caption(LONG_NAME)
    pygame.display.set_icon(assets.ICON_IMAGE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    background = BackgroundDrawer(screen, assets.BACKGROUND_IMAGE)

    # Initialize gamepad
    pygame.joystick.init()
    _ = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    # Get hack list
    hack_list = crawler.get_hack_list()

    selected_entry = 0
    scroll_offset = 0
    running = True
    while running:
        running, selected_entry, scroll_offset = handle_events(
            selected_entry, scroll_offset, hack_list
        )
        background.draw()
        draw(screen, selected_entry, scroll_offset, hack_list)

    # Quit Pygame
    pygame.quit()
    sys.exit()
