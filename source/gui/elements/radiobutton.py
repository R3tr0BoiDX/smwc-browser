from typing import Tuple, List

import pygame

import source.gui.assets as assets
from source.gui.elements.gui_element import GUIElement, PADDING_BETWEEN_ELEMENTS
from source.gui.helper import draw_text

RADIUS = 12
RADIUS_FILL = 7
PADDING_BETWEEN_OPTIONS = 24
OFFSET_TEXT = 8


class RadioButton(GUIElement):
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
        color_title = (
            assets.COLOR_MAJOR_SELECTED if selected else assets.COLOR_MAJOR_NORMAL
        )
        color_detail = (
            assets.COLOR_MINOR_SELECTED if selected else assets.COLOR_MINOR_NORMAL
        )

        # Draw label
        label_renderer = assets.FONT_MAJOR.render(self.label, True, color_title)
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
            topright=(label_rect.right, label_rect.bottom)
        )
        self.screen.blit(description_renderer, description_rect)

        last_width = 0
        all_rect = label_rect.union(description_rect)
        for index, value in enumerate(self.values):
            option_selected = index == self.selected_index
            color_title = (
                assets.COLOR_MAJOR_SELECTED
                if option_selected and selected
                else assets.COLOR_MAJOR_NORMAL
            )
            color_detail = (
                assets.COLOR_MINOR_SELECTED
                if option_selected and selected
                else assets.COLOR_MINOR_NORMAL
            )

            # Draw the circle
            label_rect_origin = label_renderer.get_rect()
            pos = (
                anchor[0] + (PADDING_BETWEEN_ELEMENTS // 2) + RADIUS + last_width,
                anchor[1] + label_rect_origin.centery,
            )
            if option_selected:  # infill
                pygame.draw.circle(self.screen, color_title, pos, RADIUS_FILL)
            circle_rect = pygame.draw.circle(self.screen, color_title, pos, RADIUS, 2)

            # Draw text
            text_rect = draw_text(
                self.screen,
                value,
                assets.FONT_MINOR,
                color_detail,
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
            # todo: gamepad input

    def get_value(self) -> bool:
        return self.selected_index

    def clear_value(self):
        self.selected_index = 0
