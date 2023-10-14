from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.elements.gui_element import GUIElement, PADDING_BETWEEN_ELEMENTS


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

    def draw(self, anchor: Tuple[int, int], selected: bool):
        color = assets.COLOR_MAJOR_SELECTED if selected else assets.COLOR_MAJOR_NORMAL
        color_detail = (
            assets.COLOR_MINOR_SELECTED if selected else assets.COLOR_MINOR_NORMAL
        )

        # Draw label
        label_renderer = assets.FONT_MAJOR.render(self.label, True, color)
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
        description_renderer = assets.FONT_MINOR.render(
            self.description, True, color_detail
        )
        description_rect = description_renderer.get_rect(
            right=label_rect.right, top=label_rect.bottom
        )
        self.screen.blit(description_renderer, description_rect)

        # Draw selected item
        label_rect_origin = label_renderer.get_rect()
        selected_entry_renderer = assets.FONT_MAJOR.render(
            self.entries[self.selected_index], True, color
        )
        text_rect = selected_entry_renderer.get_rect(
            topleft=(
                anchor[0] + (PADDING_BETWEEN_ELEMENTS // 2),
                label_rect_origin.top + anchor[1],
            )
        )
        self.screen.blit(selected_entry_renderer, text_rect)

        return label_rect.unionall([description_rect, text_rect])

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.entries)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.entries)

        elif event.type == pygame.JOYHATMOTION:
            if event.value[0] == -1:  # D-pad left
                self.selected_index = (self.selected_index - 1) % len(self.entries)
            elif event.value[0] == 1:  # D-pad right
                self.selected_index = (self.selected_index + 1) % len(self.entries)

    def get_value(self) -> int:
        return self.selected_index

    def clear_value(self):
        self.selected_index = 0
