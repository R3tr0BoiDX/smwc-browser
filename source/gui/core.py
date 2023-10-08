from abc import ABC, abstractmethod
from typing import Tuple

import pygame


class GUIElement(ABC):
    @abstractmethod
    def __init__(
        self,
        screen: pygame.Surface,
        label: str,
        font: pygame.font.Font,
    ):
        pass

    @abstractmethod
    def draw(self, pos: Tuple[int, int], selected: bool):
        # todo: second pos, one pos for right sighted alignment of label
        #  other pos for left sighted alignment of control element
        # todo as well: provide description text to be rendered underneath
        pass

    @abstractmethod
    def active(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def get_value(self):
        pass
