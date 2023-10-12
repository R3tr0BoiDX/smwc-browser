from abc import ABC, abstractmethod
from typing import Tuple

import pygame

PADDING_BETWEEN_ELEMENTS = 24

# todo: extract draw label and description to here


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
