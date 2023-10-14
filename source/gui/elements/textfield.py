from typing import Tuple
import time

import pygame

import source.gui.assets as assets
from source.gui.elements import base
from source.gui.helper import cut_string_to_width, get_major_color

SIZE = (256, 32)
OFFSET_LEFT = 8

BLINK_SPEED = 0.5  # seconds

# Define a list of allowed keycodes for a-z, 0-9, and special characters
ALLOWED_KEYCODES = list(range(32, 127))


class Textfield(base.GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        description: str,
    ):
        self.screen = screen
        self.label = label
        self.description = description
        self.text = None
        self.cursor_visible = True
        self.cursor_timer = time.time()
        self.shift_pressed = False  # Flag to track if the Shift key is pressed

    def draw(self, anchor: Tuple[int, int], selected: bool):
        label_rect = base.draw_label(self.screen, self.label, anchor, selected)
        description_rect = base.draw_description(
            self.screen, self.description, label_rect.bottomright, selected
        )

        # Draw the textbox
        box_rect = pygame.Rect(
            (base.PADDING_BETWEEN_ELEMENTS // 2) + anchor[0],
            label_rect.centery - label_rect.top - (SIZE[1] // 2) + anchor[1],
            SIZE[0],
            SIZE[1],
        )
        color = get_major_color(selected)
        pygame.draw.rect(self.screen, color, box_rect, 2)

        # Draw the text in the textbox, ensuring it doesn't exceed the maximum length
        text = cut_string_to_width(
            self.text, assets.FONT_MAJOR, box_rect.width - OFFSET_LEFT
        )
        input_text = assets.FONT_MAJOR.render(text, True, color)
        input_rect = input_text.get_rect(
            topleft=(
                box_rect.left + OFFSET_LEFT,
                box_rect.centery
                - box_rect.top
                - (input_text.get_height() // 2)
                + anchor[1],
            )
        )
        self.screen.blit(input_text, input_rect)

        # Draw cursor
        if selected:
            if time.time() - self.cursor_timer > BLINK_SPEED:
                self.cursor_timer = time.time()
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                cursor_x = input_rect.right + 2
                cursor_rect = pygame.Rect(
                    cursor_x, input_rect.y + 4, 2, input_rect.height - 10
                )
                pygame.draw.rect(self.screen, color, cursor_rect)

        return label_rect.unionall([description_rect, box_rect])

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.unicode != "":
            if event.key == pygame.K_BACKSPACE:
                if self.text is not None:
                    self.text = self.text[:-1]
            elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.shift_pressed = True

            elif self.shift_pressed:
                # Check if Shift is pressed and the key's unicode value is within the allowed keycodes
                if ord(event.unicode) in ALLOWED_KEYCODES:
                    self.add_char_to_text(event.unicode.upper())

            elif event.unicode.isalnum() or ord(event.unicode) in ALLOWED_KEYCODES:
                self.add_char_to_text(event.unicode)

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.shift_pressed = False

    def add_char_to_text(self, char: str):
        if self.text is None:
            self.text = char
        else:
            self.text += char

    def get_value(self) -> str:
        return self.text

    def clear_value(self):
        self.text = None
