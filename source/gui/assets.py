import pygame

# Images
CHECKBOX_OFF_IMAGE = pygame.image.load("media/images/checkbox_off.png")
CHECKBOX_ON_IMAGE = pygame.image.load("media/images/checkbox_on.png")
CURSOR_IMAGE = pygame.image.load("media/images/cursor.png")
LOGO_IMAGE = pygame.image.load("media/images/logo.png")
Y_BUTTON_IMAGE = pygame.image.load("media/images/y_button.png")
F_KEY_IMAGE = pygame.image.load("media/images/f_key.png")
ICON_IMAGE = pygame.image.load("media/images/icon.png")
BACKGROUND_IMAGE = pygame.image.load("media/images/background.png")
CHECK_IMAGE = pygame.image.load("media/images/check.png")


# Colors
BG_COLOR = (29, 30, 38)
ENTRY_NORMAL = (221, 221, 221)
ENTRY_SELECTED = (255, 207, 41)
DETAIL_NORMAL = (105, 118, 136)
DETAIL_SELECTED = (143, 183, 239)
SEPARATOR_COLOR = (62, 62, 69)
ARROW_COLOR = (214, 71, 24)

# Font
pygame.font.init()
FONT_TYPEFACE = "media/fonts/retro_gaming.ttf"
FONT_SIZE_TITLE = 24
FONT_SIZE_DETAIL = 16
FONT_TITLE = pygame.font.Font(FONT_TYPEFACE, FONT_SIZE_TITLE)
FONT_DETAIL = pygame.font.Font(FONT_TYPEFACE, FONT_SIZE_DETAIL)