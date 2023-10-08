import pygame

SCROLL_SPEED_X = 1
SCROLL_SPEED_Y = 1


class BackgroundDrawer:
    def __init__(
        self, screen: pygame.Surface, background_image: pygame.Surface
    ) -> None:
        self.screen = screen
        self.background_image = background_image
        self.bg_width, self.bg_height = background_image.get_size()
        self.last_pos = (0, 0)

    # Function to draw and scroll the background
    def draw(self):
        x, y = self.last_pos
        screen_width, screen_height = self.screen.get_size()

        # Scroll the background
        x += SCROLL_SPEED_X
        y += SCROLL_SPEED_Y

        # Wrap the background horizontally
        if x > 0:
            x = -self.bg_width

        # Wrap the background vertically
        if y > 0:
            y = -self.bg_height

        for i in range(x, screen_width, self.bg_width):
            for j in range(y, screen_height, self.bg_height):
                self.screen.blit(self.background_image, (i, j))

        self.last_pos = (x, y)
