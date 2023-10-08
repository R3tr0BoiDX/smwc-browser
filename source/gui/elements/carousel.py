from typing import Tuple

import pygame

import source.gui.assets as assets
from source.gui.core import GUIElement


class CarouselSelect(GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        font: pygame.font.Font,
        entries: list,
    ):
        self.screen = screen
        self.label = label
        self.font = font
        self.entries = entries
        self.selected_index = 0

    def draw(
        self,
        pos: Tuple[int, int],
        selected: bool,
    ):
        color = assets.ENTRY_SELECTED if selected else assets.ENTRY_NORMAL

        # Draw label
        label_renderer = self.font.render(self.label, True, color)
        self.screen.blit(label_renderer, pos)

        # Draw selected item
        label_rect = label_renderer.get_rect()

        selected_entry_renderer = self.font.render(
            self.entries[self.selected_index], True, color
        )
        text_rect = pygame.Rect(
            label_rect.right + pos[0],
            label_rect.centery - (selected_entry_renderer.get_height() // 2) + pos[1],
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
