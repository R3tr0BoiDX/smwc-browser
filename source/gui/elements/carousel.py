from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.elements.gui_element import GUIElement
from source.gui.constants import PADDING_BETWEEN_ELEMENTS


class CarouselSelect(GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        description: str,
        entries: list,
    ):
        self.screen = screen
        self.label = label
        self.description = description
        self.entries = entries
        self.selected_index = 0

    def draw(
        self,
        anchor: Tuple[int, int],
        selected: bool,
    ):
        color = assets.ENTRY_SELECTED if selected else assets.ENTRY_NORMAL
        color_detail = assets.DETAIL_SELECTED if selected else assets.DETAIL_NORMAL

        # Draw label
        label_renderer = assets.FONT_TITLE.render(self.label, True, color)
        label_rect = label_renderer.get_rect()
        label_rect.x = anchor[0] - (PADDING_BETWEEN_ELEMENTS // 2) - label_rect.right
        label_rect.y = anchor[1]
        self.screen.blit(label_renderer, label_rect)

        # Draw description underneath label
        description_renderer = assets.FONT_DETAIL.render(
            self.description, True, color_detail
        )
        description_rect = description_renderer.get_rect()
        description_rect.right = label_rect.right
        description_rect.y = label_rect.bottom
        self.screen.blit(description_renderer, description_rect)

        # Draw selected item
        label_rect = label_renderer.get_rect()

        selected_entry_renderer = assets.FONT_TITLE.render(
            self.entries[self.selected_index], True, color
        )
        text_rect = pygame.Rect(
            anchor[0] + (PADDING_BETWEEN_ELEMENTS // 2),
            label_rect.centery
            - (selected_entry_renderer.get_height() // 2)
            + anchor[1],
            selected_entry_renderer.get_width(),
            selected_entry_renderer.get_height(),
        )
        self.screen.blit(selected_entry_renderer, text_rect)

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.entries)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.entries)
            # todo: gamepad input

    def get_value(self) -> int:
        return self.selected_index
