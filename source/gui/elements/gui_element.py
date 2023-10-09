from abc import ABC, abstractmethod
from typing import Tuple

import pygame


class GUIElement(ABC):
    @abstractmethod
    def __init__(self, screen: pygame.Surface, label: str, description: str):
        pass

    @abstractmethod
    def draw(self, anchor: Tuple[int, int], selected: bool):
        pass

    @abstractmethod
    def active(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def get_value(self):
        pass
