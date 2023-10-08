from abc import ABC, abstractmethod
from typing import Tuple

import pygame

# Colors
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)


class GUIElement(ABC):
    @abstractmethod
    def __init__(
        self,
        screen: pygame.Surface,
        pos: Tuple[int, int],
        label: str,
        font: pygame.font.Font,
    ):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def active(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def get_value(self):
        pass
