from collections import deque
from typing import Tuple
import logging

import pygame

from source.gui.helper import draw_text, cut_string_to_width
from source.gui.assets import COLOR_MINOR_NORMAL, FONT_LOG
from source.gui.constants import LOGO_HEIGHT


MAX_LENGTH = LOGO_HEIGHT // FONT_LOG.get_height()

COLOR_WARN = (255, 207, 41)
COLOR_ERROR = (214, 71, 24)
COLOR_UNKNOWN = (255, 0, 255)


class ScreenLogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.screen_logger = ScreenLogger()

    def emit(self, record):
        log_level = record.levelname
        log_message = self.format(record)
        self.screen_logger.add_entry((log_message, log_level))


class ScreenLogger:
    def __init__(self) -> None:
        self.deque = deque(maxlen=MAX_LENGTH)

    def add_entry(self, msg: Tuple[str, str]):
        self.deque.append(msg)

    def draw(self, screen: pygame.Surface, pos: Tuple[int, int], width: int) -> None:
        msgs = list(self.deque)[::-1]  # slice to reverse
        text_y = pos[1]
        for msg in msgs:
            color = get_log_level_color(msg[1])

            level_text = f" [{msg[1]}]"
            level_width = FONT_LOG.size(level_text)[0]
            text = (
                cut_string_to_width(
                    msg[0], FONT_LOG, width - level_width, cut_right=True
                )
                + level_text
            )

            text_rect = draw_text(
                screen,
                text,
                FONT_LOG,
                color,
                (pos[0] - FONT_LOG.size(text)[0], text_y),
            )
            text_y += text_rect.height


def get_log_level_color(level: str) -> Tuple[int, int, int]:
    if level.upper() == "INFO":
        return COLOR_MINOR_NORMAL

    if level.upper() == "WARNING":
        return COLOR_WARN

    if level.upper() in ["ERROR", "CRITICAL"]:
        return COLOR_ERROR

    return COLOR_UNKNOWN
