from abc import ABC, abstractmethod
from typing import Tuple

import pygame

from source.gui import assets
from source.gui.helper import get_minor_color

PADDING_BETWEEN_ELEMENTS = 24


class GUIElement(ABC):
    @abstractmethod
    def __init__(self, screen: pygame.Surface, label: str, description: str):
        pass

    @abstractmethod
    def draw(self, anchor: Tuple[int, int], selected: bool) -> pygame.Rect:
        pass

    @abstractmethod
    def active(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def clear_value(self):
        pass


def draw_label(
    screen: pygame.Surface, label: str, anchor: Tuple[int, int], selected: bool
) -> pygame.Rect:
    color = get_minor_color(selected)

    # Draw label
    label_renderer = assets.FONT_MAJOR.render(label, True, color)
    pos = (
        anchor[0] - (PADDING_BETWEEN_ELEMENTS // 2) - label_renderer.get_width(),
        anchor[1],
    )
    text_rect = label_renderer.get_rect(topleft=pos)
    screen.blit(label_renderer, text_rect)

    return text_rect


def draw_description(
    screen: pygame.Surface, description: str, anchor: Tuple[int, int], selected: bool
) -> pygame.Rect:
    color = get_minor_color(selected)

    # Draw description underneath label
    description_renderer = assets.FONT_MINOR.render(description, True, color)
    description_rect = description_renderer.get_rect(topright=(anchor[0], anchor[1]))
    screen.blit(description_renderer, description_rect)

    return description_rect
