import pygame

from source.gui.helper import scale_image

# Images
# x3
BUTTON_A_IMAGE = scale_image(pygame.image.load("media/images/button_a.png"), 3)
BUTTON_B_IMAGE = scale_image(pygame.image.load("media/images/button_b.png"), 3)
BUTTON_X_IMAGE = scale_image(pygame.image.load("media/images/button_x.png"), 3)
BUTTON_Y_IMAGE = scale_image(pygame.image.load("media/images/button_y.png"), 3)
BUTTON_START_IMAGE = scale_image(pygame.image.load("media/images/button_start.png"), 3)
KEY_BACKSPACE_IMAGE = scale_image(pygame.image.load("media/images/key_backspace.png"), 3)
KEY_ESC_IMAGE = scale_image(pygame.image.load("media/images/key_esc.png"), 3)
KEY_F_IMAGE = scale_image(pygame.image.load("media/images/key_f.png"), 3)
KEY_RETURN_IMAGE = scale_image(pygame.image.load("media/images/key_return.png"), 3)
KEY_SPACE_IMAGE = scale_image(pygame.image.load("media/images/key_space.png"), 3)
# x2
CHECKBOX_OFF_IMAGE = scale_image(pygame.image.load("media/images/checkbox_off.png"), 2)
CHECKBOX_ON_IMAGE = scale_image(pygame.image.load("media/images/checkbox_on.png"), 2)
CURSOR_IMAGE = scale_image(pygame.image.load("media/images/cursor.png"), 2)
# x1
CHECK_IMAGE = pygame.image.load("media/images/check.png")
BACKGROUND_IMAGE = pygame.image.load("media/images/background.png")
LOGO_IMAGE = pygame.image.load("media/images/logo.png")
ICON_IMAGE = pygame.image.load("media/images/icon.png")

# Colors
COLOR_BACKGROUND = (29, 30, 38)
COLOR_MAJOR_NORMAL = (221, 221, 221)
COLOR_MAJOR_SELECTED = (255, 207, 41)
COLOR_MINOR_NORMAL = (105, 118, 136)
COLOR_MINOR_SELECTED = (143, 183, 239)
COLOR_SEPARATOR = (62, 62, 69)

# Font
pygame.font.init()
FONT_TYPEFACE = "media/fonts/retro_gaming.ttf"
FONT_SIZE_MAJOR = 24
FONT_SIZE_MINOR = 16
FONT_MAJOR = pygame.font.Font(FONT_TYPEFACE, FONT_SIZE_MAJOR)
FONT_MINOR = pygame.font.Font(FONT_TYPEFACE, FONT_SIZE_MINOR)
