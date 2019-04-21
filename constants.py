import pygame


FPS = 8
WINDOWWIDTH = 640 + 320
WINDOWHEIGHT = 480 + 240
CELLSIZE = 8
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
MAX_DIRTINESS = 10
MIN_DIRTINESS = 0
assert MAX_DIRTINESS > (MIN_DIRTINESS + 3)  # Make sure there's at least a bit of difference
MED_DIRTINESS = int((MAX_DIRTINESS - MIN_DIRTINESS) / 2)
NUM_OBSTACLES = 165
NUM_PETS = 77
NUM_ROOMBAS = 31
MAX_DIST_WITHOUT_TURNING = int(min(CELLWIDTH, CELLHEIGHT) / 3)
NUM_DROPS = 42

#                   R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 131, 24)
DARKORANGE = (181, 94, 17)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
GRAY = (120, 120, 120)
NU_PURPLE = (91, 59, 140)
LIGHT_NU_PURPLE = (204, 196, 223)
FURNITURE = (57, 134, 255)
PET = (204, 59, 151)
DIRT = (163, 116, 75)
HEAVYDIRT = (153, 78, 0)
DROP = (232, 57, 255)
TILE = (253, 246, 227)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

pygame.init()

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
