import math
from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.core import GUIElement

SIZE = (256, 32)
OFFSET_LEFT = 8

BLINK_SPEED = 30


class Textfield(GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        font: pygame.font.Font,
    ):
        self.screen = screen
        self.label = label
        self.font = font
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

    def draw(self, pos: Tuple[int, int], selected: bool):
        color = assets.ENTRY_SELECTED if selected else assets.ENTRY_NORMAL

        # Draw the label
        label_renderer = self.font.render(self.label, True, color)
        self.screen.blit(label_renderer, pos)

        # Draw the textbox
        label_rect = label_renderer.get_rect()
        box_rect = pygame.Rect(
            label_rect.right + pos[0],
            label_rect.centery - (SIZE[1] // 2) + pos[1],
            SIZE[0],
            SIZE[1],
        )
        pygame.draw.rect(self.screen, color, box_rect, 2)

        # Calculate the maximum number of characters that can fit in the textbox
        # todo: still a bit glitchy, needs some refinement
        if self.text != "":
            font_size = self.font.size(self.text)
            char_size = math.ceil(font_size[0] / len(self.text))
            max_chars = (box_rect.width - OFFSET_LEFT) // char_size
        else:
            max_chars = 0

        # Draw the text in the textbox, ensuring it doesn't exceed the maximum length
        input_text = self.font.render(self.text[-max_chars:], True, color)
        input_rect = input_text.get_rect()
        input_rect.topleft = (
            box_rect.x + OFFSET_LEFT,
            label_rect.centery - (input_rect.height // 2) + pos[1],
        )
        self.screen.blit(input_text, input_rect)

        # Draw cursor
        if selected:
            self.cursor_timer += 1
            if self.cursor_timer >= BLINK_SPEED:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

            if self.cursor_visible:
                cursor_x = (
                    input_rect.right + 2
                )  # Position the cursor to the right of the text
                cursor_rect = pygame.Rect(
                    cursor_x,
                    input_rect.y,
                    2,  # Cursor width
                    input_rect.height,
                )
                pygame.draw.rect(self.screen, color, cursor_rect)

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def get_value(self) -> str:
        return self.text
