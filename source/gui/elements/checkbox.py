from typing import Tuple

import pygame

from source.gui.core import BLACK, GUIElement

SIZE = (16, 16)


class Checkbox(GUIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        pos: Tuple[int, int],
        label: str,
        font: pygame.font.Font,
    ):
        self.screen = screen
        self.pos = pos
        self.label = label
        self.font = font
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.checked = False

    def draw(
        self,
    ):
        # Render the label
        label_renderer = self.font.render(self.label, True, BLACK)
        self.screen.blit(label_renderer, self.pos)

        # Draw the checkbox
        label_rect = label_renderer.get_rect()
        self.rect = pygame.Rect(
            label_rect.right + self.pos[0],
            label_rect.centery - (SIZE[1] // 2) + self.pos[1],
            SIZE[0],
            SIZE[1],
        )
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)

        # Draw checked
        if self.checked:
            pygame.draw.line(
                self.screen,
                BLACK,
                (self.rect.left, self.rect.centery),
                (self.rect.centerx, self.rect.bottom),
                2,
            )
            pygame.draw.line(
                self.screen,
                BLACK,
                (self.rect.centerx, self.rect.bottom),
                (self.rect.right, self.rect.top),
                2,
            )

    def active(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse input
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
        elif event.type == pygame.KEYDOWN:
            # Keyboard input
            if event.key == pygame.K_RETURN:
                self.checked = not self.checked
        # todo: gamepad input

    def get_value(self) -> bool:
        return self.checked
