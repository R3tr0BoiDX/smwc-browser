from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.elements import base


class CarouselSelect(base.GUIElement):
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
        label_rect = base.draw_label(self.screen, self.label, anchor, selected)
        description_rect = base.draw_description(
            self.screen, self.description, label_rect.bottomright, selected
        )

        # Draw selected item
        color = base.get_major_color(selected)
        selected_entry_renderer = assets.FONT_MAJOR.render(
            self.entries[self.selected_index], True, color
        )
        text_rect = selected_entry_renderer.get_rect(
            topleft=(
                anchor[0] + (base.PADDING_BETWEEN_ELEMENTS // 2),
                anchor[1],
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
