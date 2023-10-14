from typing import Tuple

import pygame

from source.gui import assets
from source.gui.elements import base
from source.gui.helper import get_major_color

SIZE = (24, 24)


class Checkbox(base.GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        description: str,
    ):
        self.screen = screen
        self.label = label
        self.description = description
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.checked = False

    def draw(self, anchor: Tuple[int, int], selected: bool) -> pygame.Rect:
        label_rect = base.draw_label(self.screen, self.label, anchor, selected)
        description_rect = base.draw_description(
            self.screen, self.description, label_rect.bottomright, selected
        )

        # Draw the checkbox
        self.rect = pygame.Rect(
            (base.PADDING_BETWEEN_ELEMENTS // 2) + anchor[0],
            label_rect.centery - label_rect.top - (SIZE[1] // 2) + anchor[1],
            SIZE[0],
            SIZE[1],
        )

        color = get_major_color(selected)
        pygame.draw.rect(self.screen, color, self.rect, 2)

        # Draw checked mark if checked
        if self.checked:
            image_size = assets.CHECK_IMAGE.get_rect()
            self.screen.blit(
                assets.CHECK_IMAGE,
                (
                    self.rect.centerx - image_size.width // 2,
                    self.rect.centery - image_size.height // 2,
                ),
            )

        return label_rect.unionall([description_rect, self.rect])

    def active(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse input
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
        elif event.type == pygame.KEYDOWN:
            # Keyboard input
            if event.key == pygame.K_SPACE:
                self.checked = not self.checked

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # A button on the gamepad
                self.checked = not self.checked

    def get_value(self) -> bool:
        return self.checked

    def clear_value(self):
        self.checked = False
