from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.elements.gui_element import GUIElement
from source.gui.constants import PADDING_BETWEEN_ELEMENTS

SIZE = (24, 24)


class Checkbox(GUIElement):
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
        color_title = assets.ENTRY_SELECTED if selected else assets.ENTRY_NORMAL
        color_detail = assets.DETAIL_SELECTED if selected else assets.DETAIL_NORMAL

        # Draw label
        label_renderer = assets.FONT_TITLE.render(self.label, True, color_title)
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
            topright=(label_rect.right, label_rect.bottom)
        )
        self.screen.blit(description_renderer, description_rect)

        # Draw the checkbox
        label_rect_origin = label_renderer.get_rect()
        self.rect = pygame.Rect(
            (PADDING_BETWEEN_ELEMENTS // 2) + anchor[0],
            label_rect_origin.centery - (SIZE[1] // 2) + anchor[1],
            SIZE[0],
            SIZE[1],
        )
        pygame.draw.rect(self.screen, color_title, self.rect, 2)

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
        # todo: gamepad input

    def get_value(self) -> bool:
        return self.checked

    def clear_value(self):
        self.checked = False
