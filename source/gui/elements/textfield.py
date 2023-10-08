from typing import Tuple
import math

import pygame

from source.gui.core import GUIElement, BLACK

SIZE = (256, 32)
OFFSET_LEFT = 8


class Textfield(GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        pos: Tuple[int, int],
        label: str,
        font: pygame.font.Font,
    ):
        self.screen = screen
        self.pos = pos
        self.label = label
        self.font = font
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.text = ""

    def draw(self):
        # Draw the label
        label_renderer = self.font.render(self.label, True, BLACK)
        self.screen.blit(label_renderer, self.pos)

        # Draw the textbox
        label_rect = label_renderer.get_rect()
        self.rect = pygame.Rect(
            label_rect.right + self.pos[0],
            label_rect.centery - (SIZE[1] // 2) + self.pos[1],
            SIZE[0],
            SIZE[1],
        )
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)

        # Calculate the maximum number of characters that can fit in the textbox
        if self.text != "":
            font_size = self.font.size(self.text)
            char_size = math.ceil(font_size[0] / len(self.text))
            max_chars = (self.rect.width - OFFSET_LEFT) // char_size
        else:
            max_chars = 0

        # Draw the text in the textbox, ensuring it doesn't exceed the maximum length
        input_text = self.font.render(self.text[-max_chars:], True, BLACK)
        input_rect = input_text.get_rect()
        input_rect.topleft = (
            self.rect.x + OFFSET_LEFT,
            label_rect.centery - (input_rect.height // 2) + self.pos[1],
        )
        self.screen.blit(input_text, input_rect)

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def get_value(self) -> str:
        return self.text
