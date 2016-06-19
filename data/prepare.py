import os
import pygame as pg
from . import tools


SCREEN_SIZE = (480, 640)
ORIGINAL_CAPTION = "Pygame-Calculator"
BG_COLOR = [(0xffb900),(0xe74856),(0x0078d7),(0x0099bc),(0x7a7574),(0x767676),\
            (0xff8c00),(0xe81123),(0x0063b1),(0x2d7d9a),(0x5d5a58),(0x4c4a48),\
            (0xf7630c),(0xea005e),(0x8e8cd8),(0x00b7c3),(0x68768a),(0x69797e),\
            (0xca5010),(0xc30052),(0x6b69d6),(0x038387),(0x515c6b),(0x4a5459),\
            (0xda3b01),(0xe3008c),(0x8764b8),(0x00b294),(0x567c73),(0x647c64),\
            (0xef6950),(0xbf0077),(0x744da9),(0x018574),(0x486860),(0x525e54),\
            (0xd13438),(0xc239b3),(0xb146c2),(0x00cc6a),(0x498205),(0x847545),\
            (0xff4343),(0x9a0089),(0x881798),(0x10893e),(0x107c10),(0x7e735f)]

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
SFX = tools.load_all_sfx(os.path.join("resources", "sound"))

