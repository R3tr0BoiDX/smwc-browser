import sys
import logging

import pygame

from source.smwc import crawler
from source import file
from source.product_name import LONG_NAME

pygame.init()

WIDTH, HEIGHT = 1280, 1000

# Colors
BG_COLOR = (29, 30, 38)
ENTRY_NORMAL = (221, 221, 221)
ENTRY_SELECTED = (171, 200, 239)
DETAIL_NORMAL = (105, 118, 136)
DETAIL_SELECTED = (143, 183, 239)
SEPARATOR_COLOR = (62, 62, 69)
ARROW_COLOR = (214, 71, 24)

# Fonts
FONT_SIZE_TITLE = 24
FONT_SIZE_DETAILS = 16
FONT_TITLE = pygame.font.Font("media/fonts/retro_gaming.ttf", FONT_SIZE_TITLE)
FONT_DETAILS = pygame.font.Font("media/fonts/retro_gaming.ttf", FONT_SIZE_DETAILS)

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
CURSOR_SCALE_FACTOR = 2
SELECTION_INDENT = 16

# Menu
MENU_HEIGHT = HEIGHT - HEADER_TOTAL - FOOTER_HEIGHT
MENU_ENTRY_HEIGHT = 96  # px

# Check box
CHECKBOX_OFFSET = 16  # y
CHECKBOX_DEMO_OFFSET = CURSOR_OFFSET[0] + 32  # x
CHECKBOX_FEATURED_OFFSET = CHECKBOX_DEMO_OFFSET + 48  # x
CHECK_BOX_SCALE_FACTOR = CURSOR_SCALE_FACTOR  # x

# Text
TEXT_OFFSET = CHECKBOX_FEATURED_OFFSET + 48  # x
NAME_OFFSET = 16  # y
AUTHOR_OFFSET = 8  # x
DIFFICULTY_OFFSET = NAME_OFFSET + 32  # y
DETAIL_OFFSET = DIFFICULTY_OFFSET + 24  # y

# Images
BACKGROUND_IMAGE = pygame.image.load("media/images/background.png")
CHECKBOX_OFF_IMAGE = pygame.image.load("media/images/checkbox_off.png")
CHECKBOX_ON_IMAGE = pygame.image.load("media/images/checkbox_on.png")
CURSOR_IMAGE = pygame.image.load("media/images/cursor.png")
LOGO_IMAGE = pygame.image.load("media/images/logo.png")
Y_BUTTON_IMAGE = pygame.image.load("media/images/y_button.png")
F_KEY_IMAGE = pygame.image.load("media/images/f_key.png")

logger = logging.getLogger(__name__)


def scale_image(image: pygame.Surface, scale_factor: float) -> pygame.Surface:
    scaled_width = image.get_width() * scale_factor
    scaled_height = image.get_height() * scale_factor
    return pygame.transform.scale(image, (scaled_width, scaled_height))


def draw_text(
    screen: pygame.Surface, text: str, font: pygame.font.Font, color: tuple, pos: tuple
) -> None:
    text_rendered = font.render(text, True, color)
    text_rect = text_rendered.get_rect(topleft=pos)
    screen.blit(text_rendered, text_rect)


def draw_checkbox(
    screen: pygame.Surface, state: bool, entry_y_pos: int, offset_x: int
) -> None:
    image = CHECKBOX_ON_IMAGE if state else CHECKBOX_OFF_IMAGE
    offset_y = entry_y_pos + CHECKBOX_OFFSET
    screen.blit(image, (offset_x, offset_y))


# Get the dimensions of the background image
bg_width, bg_height = BACKGROUND_IMAGE.get_size()

# Define the speed at which the background scrolls
SCROLL_SPEED_X = 1
SCROLL_SPEED_Y = 1


# Function to draw and scroll the background
def draw_background(screen: pygame.Surface, last_pos):
    x, y = last_pos

    # Scroll the background
    x += SCROLL_SPEED_X
    y += SCROLL_SPEED_Y

    # Wrap the background horizontally
    if x > 0:
        x = -bg_width

    # Wrap the background vertically
    if y > 0:
        y = -bg_height

    for i in range(x, WIDTH, bg_width):
        for j in range(y, HEIGHT, bg_height):
            screen.blit(BACKGROUND_IMAGE, (i, j))

    return x, y


CHECKBOX_ON_IMAGE = scale_image(CHECKBOX_ON_IMAGE, CHECK_BOX_SCALE_FACTOR)
CHECKBOX_OFF_IMAGE = scale_image(CHECKBOX_OFF_IMAGE, CHECK_BOX_SCALE_FACTOR)
CURSOR_IMAGE = scale_image(CURSOR_IMAGE, CURSOR_SCALE_FACTOR)
Y_BUTTON_IMAGE = scale_image(Y_BUTTON_IMAGE, 3)
F_KEY_IMAGE = scale_image(F_KEY_IMAGE, 3)


# Main loop
def draw_header(screen: pygame.Surface):
    screen.blit(LOGO_IMAGE, ((WIDTH - LOGO_IMAGE.get_width()) // 2, LOGO_PADDING_Y))
    draw_text(
        screen,
        "Demo | Featured | Hack details",
        FONT_DETAILS,
        DETAIL_NORMAL,
        (DESCRIPTION_OFFSET[0], HEADER_TOTAL - DESCRIPTION_OFFSET[1]),
    )


def draw_footer(screen: pygame.Surface):
    footer_y = HEIGHT - Y_BUTTON_IMAGE.get_width() - FOOTER_OFFSET[1]
    screen.blit(Y_BUTTON_IMAGE, (FOOTER_OFFSET[0], footer_y))

    slash_x = FOOTER_OFFSET[0] + Y_BUTTON_IMAGE.get_width()
    draw_text(screen, "/", FONT_DETAILS, DETAIL_NORMAL, (slash_x, footer_y))

    f_key_x = slash_x + FONT_DETAILS.size("/")[0]
    screen.blit(F_KEY_IMAGE, (f_key_x, footer_y))

    filter_text_x = f_key_x + F_KEY_IMAGE.get_width()
    draw_text(
        screen, ": Apply filter", FONT_DETAILS, DETAIL_NORMAL, (filter_text_x, footer_y)
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
            ENTRY_NORMAL if not is_selected else ENTRY_SELECTED,
            (TEXT_OFFSET + indent, entry_y + NAME_OFFSET),
        )

        # author
        name_text_width, _ = FONT_TITLE.size(entry.name)
        draw_text(
            screen,
            f"by {entry.author}",
            FONT_DETAILS,
            ENTRY_NORMAL if not is_selected else ENTRY_SELECTED,
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
            DETAIL_NORMAL if not is_selected else DETAIL_SELECTED,
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
            DETAIL_NORMAL if not is_selected else DETAIL_SELECTED,
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
        SEPARATOR_COLOR,
        (SEPARATOR_OFFSET, separator_y),
        (WIDTH - SEPARATOR_OFFSET, separator_y),
        1,
    )


def draw(
    screen: pygame.Surface,
    selected_entry: int,
    scroll_offset: int,
    hack_list: list,
    bg_pos: tuple,
):
    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw GUI
    bg_pos = draw_background(screen, bg_pos)
    draw_header(screen)
    draw_footer(screen)
    draw_hack_list(screen, selected_entry, scroll_offset, hack_list)

    # Update the display
    pygame.display.flip()

    return bg_pos


def handle_events(selected_entry: int, scroll_offset: int, hack_list: list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, selected_entry, scroll_offset
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_entry = max(0, selected_entry - 1)
                if selected_entry < scroll_offset:
                    scroll_offset = selected_entry
            elif event.key == pygame.K_DOWN:
                selected_entry = min(len(hack_list) - 1, selected_entry + 1)
                if selected_entry >= scroll_offset + MENU_HEIGHT // MENU_ENTRY_HEIGHT:
                    scroll_offset = min(
                        len(hack_list) - MENU_HEIGHT // MENU_ENTRY_HEIGHT,
                        selected_entry - MENU_HEIGHT // MENU_ENTRY_HEIGHT + 1,
                    )
            elif event.key == pygame.K_RETURN:
                logger.info("Selected: %s", hack_list[selected_entry].name)
                file.download_and_run(hack_list[selected_entry].download_url)
            elif event.key == pygame.K_ESCAPE:
                return False, selected_entry, scroll_offset

    return True, selected_entry, scroll_offset


def run():
    # Initialize screen
    pygame.display.set_caption(LONG_NAME)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Get hack list
    hack_list = crawler.get_hack_list()

    selected_entry = 0
    scroll_offset = 0
    bg_pos = (0, 0)
    running = True
    while running:
        running, selected_entry, scroll_offset = handle_events(
            selected_entry, scroll_offset, hack_list
        )
        bg_pos = draw(screen, selected_entry, scroll_offset, hack_list, bg_pos)

    # Quit Pygame
    pygame.quit()
    sys.exit()
