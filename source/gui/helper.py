from typing import Tuple, Union, List
import math

import pygame


def cut_string_to_width(
    text: str, font: pygame.font.Font, width: int, cut_right: bool = False
) -> int:
    max_chars = 0
    if not text:
        return text

    if text != "":
        char_size = math.ceil(font.size(text)[0] / len(text))
        max_chars = width // char_size

    if len(text) > max_chars:
        max_chars -= 3
        if cut_right:
            return text[:max_chars] + "..."
        return "..." + text[-max_chars:]
    return text


def draw_text(
    screen: pygame.Surface, text: str, font: pygame.font.Font, color: tuple, pos: tuple
) -> pygame.Rect:
    text_rendered = font.render(text, True, color)
    text_rect = text_rendered.get_rect(topleft=pos)
    screen.blit(text_rendered, text_rect)
    return text_rect


def draw_image(screen: pygame.Surface, image: pygame.Surface, pos: Tuple[int, int]):
    image_rect = image.get_rect(topleft=pos)
    screen.blit(image, image_rect)
    return image_rect


def scale_image(image: pygame.Surface, scale_factor: float) -> pygame.Surface:
    scaled_width = image.get_width() * scale_factor
    scaled_height = image.get_height() * scale_factor
    return pygame.transform.scale(image, (scaled_width, scaled_height))


def draw_footer_button(
    screen: pygame.Surface,
    text: str,
    button_image: pygame.Surface,
    key_image: Union[pygame.Surface, List[pygame.Surface]],
    font: pygame.font.Font,
    pos: Tuple[int, int],
    color: Tuple[int, int, int],
) -> pygame.Rect:
    button_rect = draw_image(screen, button_image, pos)

    slash_rendered = font.render(text, True, color).get_rect()
    slash_rect = draw_text(
        screen,
        " / ",
        font,
        color,
        (button_rect.right, button_rect.centery - (slash_rendered.height // 2)),
    )

    to_render = [key_image] if isinstance(key_image, pygame.Surface) else key_image
    keys_rect = slash_rect
    for key in to_render:
        # draw key image
        key_rendered = key.get_rect()
        key_rect = draw_image(
            screen,
            key,
            (keys_rect.right, keys_rect.centery - (key_rendered.height // 2)),
        )
        keys_rect = keys_rect.union(key_rect)

        # if not last key, draw plus sign between keys
        if key != to_render[-1]:
            plus_rendered = font.render(text, True, color).get_rect()
            plus_rect = draw_text(
                screen,
                " + ",
                font,
                color,
                (key_rect.right, key_rect.centery - (plus_rendered.height // 2)),
            )
            keys_rect = keys_rect.union(plus_rect)

    text_rendered = font.render(text, True, color).get_rect()
    text_rect = draw_text(
        screen,
        text,
        font,
        color,
        (keys_rect.right, keys_rect.centery - (text_rendered.height // 2)),
    )

    return button_rect.unionall([slash_rect, key_rect, text_rect])
