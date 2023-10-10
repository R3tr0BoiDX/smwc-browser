import math
from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.elements.gui_element import GUIElement
from source.gui.constants import PADDING_BETWEEN_ELEMENTS

SIZE = (256, 32)
OFFSET_LEFT = 8

BLINK_SPEED = 30


class Textfield(GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        description: str,
    ):
        self.screen = screen
        self.label = label
        self.description = description
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

    def draw(self, anchor: Tuple[int, int], selected: bool):
        color = assets.ENTRY_SELECTED if selected else assets.ENTRY_NORMAL
        color_detail = assets.DETAIL_SELECTED if selected else assets.DETAIL_NORMAL

        # Draw label
        label_renderer = assets.FONT_TITLE.render(self.label, True, color)
        label_rect = label_renderer.get_rect(
            topleft=(
                anchor[0]
                - (PADDING_BETWEEN_ELEMENTS // 2)
                - label_renderer.get_width(),
                anchor[1],
            )
        )
        self.screen.blit(label_renderer, label_rect)

        # Draw description underneath label
        description_renderer = assets.FONT_DETAIL.render(
            self.description, True, color_detail
        )
        description_rect = description_renderer.get_rect(
            right=label_rect.right, top=label_rect.bottom
        )
        self.screen.blit(description_renderer, description_rect)

        # Draw the textbox
        label_rect_origin = label_renderer.get_rect()
        box_rect = pygame.Rect(
            (PADDING_BETWEEN_ELEMENTS // 2) + anchor[0],
            label_rect_origin.top + anchor[1],
            SIZE[0],
            SIZE[1],
        )
        pygame.draw.rect(self.screen, color, box_rect, 2)

        # Calculate the maximum number of characters that can fit in the textbox
        if self.text != "":
            char_size = math.ceil(assets.FONT_TITLE.size(self.text)[0] / len(self.text))
            max_chars = (box_rect.width - OFFSET_LEFT) // char_size
        else:
            max_chars = 0

        # Draw the text in the textbox, ensuring it doesn't exceed the maximum length
        input_text = assets.FONT_TITLE.render(self.text[-max_chars:], True, color)
        input_rect = input_text.get_rect(
            topleft=(
                box_rect.x + OFFSET_LEFT,
                label_rect_origin.centery - (input_text.get_height() // 2) + anchor[1],
            )
        )
        self.screen.blit(input_text, input_rect)

        # Draw cursor
        if selected:
            self.cursor_timer += 1
            if self.cursor_timer >= BLINK_SPEED:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

            if self.cursor_visible:
                cursor_x = input_rect.right + 2
                cursor_rect = pygame.Rect(
                    cursor_x, input_rect.y + 4, 2, input_rect.height - 10
                )
                pygame.draw.rect(self.screen, color, cursor_rect)

        return label_rect.unionall([description_rect, box_rect])

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def get_value(self) -> str:
        return self.text

    def clear_value(self):
        self.text = ""
