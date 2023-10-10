from collections import deque
from typing import Tuple

import pygame

from source.gui.helper import draw_text
from source.gui.assets import COLOR_MINOR_NORMAL

MAX_LENGTH = 3

ENTRIES_PADDING = 4

COLOR_WARN = (255, 207, 41)
COLOR_ERROR = (214, 71, 24)
COLOR_UNKNOWN = (255, 0, 255)

# screen_logger = ScreenLogger()


# todo: finish screen logger
# class ScreenLogHandler(logging.Handler):
#     def emit(self, record):
#         log_level = record.levelname
#         log_message = self.format(record)
#         screen_logger.add_entry((log_message, log_level))


class ScreenLogger:
    def __init__(self) -> None:
        self.deque = deque(maxlen=MAX_LENGTH)

    def add_entry(self, msg: Tuple[str, str]):
        self.deque.append(msg)

    def draw(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        pos: Tuple[int, int],
    ):
        msgs = list(self.deque)[::-1]  # slice to reverse
        text_y = pos[1]
        for msg in msgs:
            color = get_log_level_color(msg[1])
            text_rect = draw_text(screen, msg[0], font, color, (pos[0], text_y))

            text_y -= text_rect.height - ENTRIES_PADDING


def get_log_level_color(level: str) -> Tuple[int, int, int]:
    if level.upper() == "INFO":
        return COLOR_MINOR_NORMAL

    if level.upper() == "WARNING":
        return COLOR_WARN

    if level.upper() in ["ERROR", "CRITICAL"]:
        return COLOR_ERROR

    return COLOR_UNKNOWN
