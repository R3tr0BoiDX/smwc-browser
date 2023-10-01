import pygame
import sys
import source.smwc.crawler as crawler
from source.product_name import LONG_NAME

pygame.init()

WIDTH, HEIGHT = 1280, 720
MENU_HEIGHT = HEIGHT

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

# Separator
SEPARATOR_OFFSET = 16  # x

# Selection
CURSOR_OFFSET = (SEPARATOR_OFFSET, 16)  # x, y
CURSOR_SCALE_FACTOR = 2
SELECTION_INDENT = 16

# Menu entry
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

# Get the dimensions of the background image
bg_width, bg_height = BACKGROUND_IMAGE.get_size()

hack_list = crawler.get_hack_list()

selected_entry = 0
scroll_offset = 0

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(LONG_NAME)


def scale_image(image, scale_factor):
    scaled_width = image.get_width() * scale_factor
    scaled_height = image.get_height() * scale_factor
    return pygame.transform.scale(image, (scaled_width, scaled_height))


def render_text(text, font, color, x, y):
    text_rendered = font.render(text, True, color)
    text_rect = text_rendered.get_rect(topleft=(x, y))
    screen.blit(text_rendered, text_rect)


def draw_checkbox(state: bool, entry_y_pos: int, offset_x: int):
    image = CHECKBOX_ON_IMAGE if state else CHECKBOX_OFF_IMAGE
    offset_y = entry_y_pos + CHECKBOX_OFFSET
    screen.blit(image, (offset_x, offset_y))


CHECKBOX_ON_IMAGE = scale_image(CHECKBOX_ON_IMAGE, CHECK_BOX_SCALE_FACTOR)
CHECKBOX_OFF_IMAGE = scale_image(CHECKBOX_OFF_IMAGE, CHECK_BOX_SCALE_FACTOR)
CURSOR_IMAGE = scale_image(CURSOR_IMAGE, CURSOR_SCALE_FACTOR)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                print(f"Selected: {hack_list[selected_entry].name}")
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Tile the background image
    for x in range(0, WIDTH, bg_width):
        for y in range(0, HEIGHT, bg_height):
            screen.blit(BACKGROUND_IMAGE, (x, y))

    # Render table-like view for hack_list
    for i in range(
        scroll_offset,
        min(len(hack_list), scroll_offset + MENU_HEIGHT // MENU_ENTRY_HEIGHT),
    ):
        entry = hack_list[i]
        is_selected = i == selected_entry
        entry_y = (i - scroll_offset) * MENU_ENTRY_HEIGHT

        indent = SELECTION_INDENT if is_selected else 0

        # name
        render_text(
            entry.name,
            FONT_TITLE,
            ENTRY_NORMAL if not is_selected else ENTRY_SELECTED,
            TEXT_OFFSET + indent,
            entry_y + NAME_OFFSET,
        )

        # author
        name_text_width, name_text_height = FONT_TITLE.size(entry.name)
        render_text(
            f"by {entry.author}",
            FONT_DETAILS,
            ENTRY_NORMAL if not is_selected else ENTRY_SELECTED,
            name_text_width + TEXT_OFFSET + AUTHOR_OFFSET + indent,
            entry_y + NAME_OFFSET + 8,
            # todo: replace 8 with actual calculated value, so title and line form one line
        )

        # difficulty
        render_text(
            entry.difficulty.value[0],
            FONT_DETAILS,
            DETAIL_NORMAL if not is_selected else DETAIL_SELECTED,
            TEXT_OFFSET + indent,
            entry_y + DIFFICULTY_OFFSET,
        )

        # details
        render_text(
            (
                f"{str(entry.rating) + '/5.0' if entry.rating else 'No ratings given'} | "
                f"{entry.length} {'exit' if entry.length == 1 else 'exits'} | "
                f"{entry.download_count} downloads | {entry.date.strftime('%c')} | {entry.size}"
            ),
            FONT_DETAILS,
            DETAIL_NORMAL if not is_selected else DETAIL_SELECTED,
            TEXT_OFFSET + indent,
            entry_y + DETAIL_OFFSET,
        )

        draw_checkbox(entry.demo, entry_y, CHECKBOX_DEMO_OFFSET + indent)
        draw_checkbox(entry.featured, entry_y, CHECKBOX_FEATURED_OFFSET + indent)

        # Render red triangle next to the selected entry
        if is_selected:
            cursor_offset_y = (
                entry_y + CURSOR_OFFSET[1] + (CURSOR_IMAGE.get_height() // 2)
            )
            screen.blit(CURSOR_IMAGE, (CURSOR_OFFSET[0] + indent, cursor_offset_y))

        # Draw a white separator line between entries
        separator_y = entry_y + MENU_ENTRY_HEIGHT
        pygame.draw.line(
            screen,
            SEPARATOR_COLOR,
            (SEPARATOR_OFFSET, separator_y),
            (WIDTH - SEPARATOR_OFFSET, separator_y),
            1,
        )

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
