from typing import Tuple, List

import pygame

from source.gui import assets
from source.gui.elements import base
from source.gui.helper import draw_text

RADIUS = 12
RADIUS_FILL = 7
PADDING_BETWEEN_OPTIONS = 24
OFFSET_TEXT = 8


class RadioButton(base.GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        description: str,
        values: List[str],
    ):
        self.screen = screen
        self.label = label
        self.description = description
        self.values = values
        self.selected_index = 0

    def draw(self, anchor: Tuple[int, int], selected: bool) -> pygame.Rect:
        label_rect = base.draw_label(self.screen, self.label, anchor, selected)
        description_rect = base.draw_description(
            self.screen, self.description, label_rect.bottomright, selected
        )

        last_width = 0
        all_rect = label_rect.union(description_rect)
        for index, value in enumerate(self.values):
            option_selected = index == self.selected_index
            color_major = base.get_major_color(option_selected)
            color_minor = base.get_minor_color(option_selected)

            # Draw the circle
            pos = (
                anchor[0] + (base.PADDING_BETWEEN_ELEMENTS // 2) + RADIUS + last_width,
                anchor[1] + (label_rect.centery - label_rect.top),
            )
            if option_selected:  # infill
                pygame.draw.circle(self.screen, color_major, pos, RADIUS_FILL)
            circle_rect = pygame.draw.circle(self.screen, color_major, pos, RADIUS, 2)

            # Draw text
            text_rect = draw_text(
                self.screen,
                value,
                assets.FONT_MINOR,
                color_minor,
                (circle_rect.right + OFFSET_TEXT, circle_rect.centery - RADIUS),
            )

            # Calculate position for next option
            option_rect = circle_rect.union(text_rect)
            last_width += option_rect.width + PADDING_BETWEEN_OPTIONS
            all_rect.union(option_rect)

        return all_rect

    def active(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.values)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.values)

        elif event.type == pygame.JOYHATMOTION:
            if event.value[0] == -1:  # D-pad left
                self.selected_index = (self.selected_index - 1) % len(self.values)
            elif event.value[0] == 1:  # D-pad right
                self.selected_index = (self.selected_index + 1) % len(self.values)

    def get_value(self) -> bool:
        return self.selected_index

    def clear_value(self):
        self.selected_index = 0
