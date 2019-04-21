# Final Project
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, math
from vehicle_agent import Vehicle
from map import Map, make_map
from constants import *
from pygame.locals import *
#
# FPS = 8
# WINDOWWIDTH = 640 + 320
# WINDOWHEIGHT = 480 + 240
# CELLSIZE = 20
# assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
# assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
# CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
# CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
# MAX_DIRTINESS = 10
# MIN_DIRTINESS = 0
# assert MAX_DIRTINESS > (MIN_DIRTINESS + 3)  # Make sure there's at least a bit of difference
# MED_DIRTINESS = int((MAX_DIRTINESS - MIN_DIRTINESS) / 2)
# NUM_OBSTACLES = 165
# NUM_PETS = 77
# NUM_ROOMBAS = 31
# MAX_DIST_WITHOUT_TURNING = int(min(CELLWIDTH, CELLHEIGHT) / 3)
# NUM_DROPS = 42
#
# #                   R    G    B
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# ORANGE = (255, 131, 24)
# DARKORANGE = (181, 94, 17)
# GREEN = (0, 255, 0)
# DARKGREEN = (0, 155, 0)
# DARKGRAY = (40, 40, 40)
# GRAY = (120, 120, 120)
# NU_PURPLE = (91, 59, 140)
# LIGHT_NU_PURPLE = (204, 196, 223)
# FURNITURE = (57, 134, 255)
# PET = (204, 59, 151)
# DIRT = (163, 116, 75)
# HEAVYDIRT = (153, 78, 0)
# DROP = (232, 57, 255)
# TILE = (253, 246, 227)
# BGCOLOR = BLACK
#
# UP = 'up'
# DOWN = 'down'
# LEFT = 'left'
# RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    # pygame.init()
    # FPSCLOCK = pygame.time.Clock()
    # DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('ALASKAN BULL WORMS!!!!!')

    show_start_screen()
    while True:
        run_game()


def run_game():
    room = make_map()

    # Set a random start point
    roombas = []
    for i in range(NUM_ROOMBAS):
        roombas.append(Vehicle(ORANGE, DARKORANGE, room))#, FPSCLOCK, DISPLAYSURF, BASICFONT))

    # pets = []
    # for pet in range(NUM_PETS):
    #     pets.append(Pet(room))

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        for roomba in roombas:
            roomba.move(room)

        # for pet in pets:
        #     pet.move(room)

        DISPLAYSURF.fill(BGCOLOR)
        draw_grid(room)

        for roomba in roombas:
            roomba.draw()

        # for pet in pets:
        #     pet.draw()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_press_key_msg():
    press_key_surf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 67)
    title_surf1 = title_font.render('ALASKAN BULL WORMS!', True, WHITE, NU_PURPLE)
    title_surf2 = title_font.render('ALASKAN BULL WORMS!', True, LIGHT_NU_PURPLE)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotated_surf2, rotated_rect2)

        draw_press_key_msg()

        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def get_random_location():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def draw_grid(room):
    for tile_row in room.tiles:
        for tile in tile_row:
            if tile is None:
                continue
            x = tile.position['x'] * CELLSIZE
            y = tile.position['y'] * CELLSIZE

            tile_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, TILE, tile_rect)

            obstacle_or_dirt_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            if tile.drop:
                pygame.draw.rect(DISPLAYSURF, BLACK, obstacle_or_dirt_rect)
            elif tile.obstacle:
                pygame.draw.rect(DISPLAYSURF, FURNITURE, obstacle_or_dirt_rect)
            elif tile.is_dirty():
                if tile.is_very_dirty():
                    pygame.draw.rect(DISPLAYSURF, HEAVYDIRT, obstacle_or_dirt_rect)
                else:
                    pygame.draw.rect(DISPLAYSURF, DIRT, obstacle_or_dirt_rect)

            pygame.draw.rect(DISPLAYSURF, GRAY, tile_rect, 4)  # 4 is the width of the rectangles' outline


# def make_map():
#     """Makes a room object that satisfies all the requirements
#
#     :return: `Room` object, consisting of a bunch of tiles
#     """
#     tiles = []
#     max_x = 0
#     max_y = 0
#     for row_idx, y in enumerate(range(0, CELLHEIGHT)):
#         # Add a list for the new row
#         tiles.append([])
#         if row_idx > max_y:
#             max_y = row_idx
#
#         for col_idx, x in enumerate(range(0, CELLWIDTH)):
#             if col_idx > max_x:
#                 max_x = col_idx
#
#             # make room irregularly shaped by omitting tiles
#             if y == 6 and x < 6:
#                 tiles[row_idx].append(None)
#                 continue
#             elif y == 11 and x > (WINDOWWIDTH / CELLSIZE) - 4:
#                 tiles[row_idx].append(None)
#                 continue
#
#             # Make big rectangular gap in middle of room
#             elif 3 * CELLWIDTH / 7 < col_idx < 4 * CELLWIDTH / 7 and 3 * CELLHEIGHT / 7 < row_idx < 4 * CELLHEIGHT / 7:
#                 tiles[row_idx].append(None)
#                 continue
#
#             dirt_level = random.randint(MIN_DIRTINESS, MAX_DIRTINESS)
#
#             # We'll handle the `drop` and `obstacle` stuff later, because we don't want to have too many drops or
#             # obstacles that the roombas can't move
#             tile = Tile(position={'x': x, 'y': y}, dirtiness=dirt_level, drop=False, obstacle=False, pet=False)
#             tiles[row_idx].append(tile)
#
#     for obstacle in range(NUM_OBSTACLES):
#         tile_col = random.randint(0, max_y)
#         tile_row = random.randint(0, max_x)
#         if tiles[tile_col][tile_row] is not None:
#             tiles[tile_col][tile_row].add_obstacle()
#
#     # for pet in range(NUM_PETS):
#     #     tile_col = random.randint(0, max_y)
#     #     tile_row = random.randint(0, max_x)
#     #     if tiles[tile_col][tile_row] is not None:
#     #         tiles[tile_col][tile_row].add_pet()
#
#     for drop in range(NUM_DROPS):
#         tile_col = random.randint(0, max_y)
#         tile_row = random.randint(0, max_x)
#         if tiles[tile_col][tile_row] is not None:
#             tiles[tile_col][tile_row].add_drop()
#
#     room = Map(tiles)
#
#     return room


# class Room:
#     def __init__(self, tiles):
#         self.tiles = tiles
#
#     def get_current_tile(self, position):
#         """Gets tile at the current position
#
#         :param position: Current position
#         :return:         Tile the roomba is currently on top of
#         """
#         return self.tiles[position['y']][position['x']]
#
#     def get_tile_up(self, position):
#         """Gets tile one tile up from current position
#
#         :param position: Current position
#         :return:         If there's a tile up from current tile, return that, otherwise return `None`
#         """
#         if position['y'] <= 0:
#             return None
#         return self.tiles[position['y'] - 1][position['x']]
#
#     def get_tile_down(self, position):
#         """Gets tile one tile down from current position
#
#         :param position: Current position
#         :return:         If there's a tile down from current tile, return that, otherwise return `None`
#         """
#         if position['y'] >= CELLHEIGHT - 1:
#             return None
#         return self.tiles[position['y'] + 1][position['x']]
#
#     def get_tile_left(self, position):
#         """Gets tile one tile left from current position
#
#         :param position: Current position
#         :return:         If there's a tile left from current tile, return that, otherwise return `None`
#         """
#         if position['x'] <= 0:
#             return None
#         return self.tiles[position['y']][position['x'] - 1]
#
#     def get_tile_right(self, position):
#         """Gets tile one tile right from current position
#
#         :param position: Current position
#         :return:         If there's a tile right from current tile, return that, otherwise return `None`
#         """
#         if position['x'] >= CELLWIDTH - 1:
#             return None
#         return self.tiles[position['y']][position['x'] + 1]


# class Tile:
#     def __init__(self, position, dirtiness, drop, obstacle, pet):
#         """Creates a `Tile` object, representing a square in the map of the room to be cleaned
#
#         :param position:  Position of the tile
#         :param dirtiness: Level of dirtiness of the tile; comes in integer gradations, 0 being clean and higher numbers
#                           being successively more dirty
#         :param drop:      Bool, whether or not there's a dropoff in elevation for this tile
#         :param obstacle:  Bool, whether or not this tile has an obstacle in it
#         :param pet:       Bool, whether or not this tile has a pet in it
#         """
#         self.position = position
#         self.dirtiness = dirtiness
#         self.drop = drop
#         self.obstacle = obstacle
#         self.pet = pet
#         self.roomba = None
#
#     def is_dirty(self):
#         return self.dirtiness > MIN_DIRTINESS
#
#     def is_very_dirty(self):
#         return self.dirtiness > MED_DIRTINESS
#
#     def can_be_dirtier(self):
#         return self.dirtiness < MAX_DIRTINESS
#
#     def clean_dirt(self):
#         """Removes dirt from tile.  If tile is quite dirty, it removes multiple dirt units at once
#
#         :return: Number of dirt units removed
#         """
#         if self.is_dirty():
#             if self.is_very_dirty():
#                 self.dirtiness -= 2  # A lot of dirt got sucked up
#                 return 2
#             else:
#                 self.dirtiness -= 1
#                 return 1
#         return 0  # If there's no dirt on this tile, we can't clean anything from it
#
#     def add_dirt(self):
#         if self.can_be_dirtier():
#             self.dirtiness += 1
#
#     def add_obstacle(self):
#         if not self.obstacle:
#             self.obstacle = True
#
#     def remove_obstacle(self):
#         if self.obstacle:
#             self.obstacle = False
#
#     def add_pet(self):
#         if not self.pet:
#             self.pet = True
#
#     def remove_pet(self):
#         if self.pet:
#             self.pet = False
#
#     def add_roomba(self, roomba):
#         if self.roomba is not None:
#             roomba.explode()
#         self.roomba = roomba
#
#     def remove_roomba(self, roomba):
#         if self.roomba != roomba:
#             # Note from Roomba owner's manual: If your Roomba explodes upon startup, this is not unexpected behavior.
#             # Please continue to enjoy your Roomba!
#             roomba.explode()
#         self.roomba = None
#
#     def add_drop(self):
#         if not self.drop:
#             self.drop = True




# class Pet:
#     def __init__(self, room):
#         startx = random.randint(5, CELLWIDTH - 6)
#         starty = random.randint(5, CELLHEIGHT - 6)
#         self.position = {'x': startx, 'y': starty}
#
#         while room.get_current_tile(self.position) is None:
#             startx = random.randint(5, CELLWIDTH - 6)
#             starty = random.randint(5, CELLHEIGHT - 6)
#
#             self.position = {'x': startx, 'y': starty}
#
#         self.directions = [RIGHT, LEFT, UP, DOWN]
#
#     def move(self, room):
#         """Pets can move anywhere without regard to what is already in the space to which they are moving.  It is up to
#         all other entities to avoid the pets (should they wish to avoid them)
#
#         :param room: `Room` object, needed make sure the pet doesn't wander through walls and stuff
#         """
#         move_direction = random.choice(self.directions)
#
#         if move_direction == UP:
#             tile_up = room.get_tile_up(self.position)
#             if tile_up is not None:
#                 current_tile = room.get_current_tile(self.position)
#                 current_tile.remove_pet()
#                 self.position['y'] -= 1
#                 tile_up.add_pet()
#
#         elif move_direction == RIGHT:
#             tile_right = room.get_tile_right(self.position)
#             if tile_right is not None:
#                 current_tile = room.get_current_tile(self.position)
#                 current_tile.remove_pet()
#                 self.position['x'] += 1
#                 tile_right.add_pet()
#
#         elif move_direction == DOWN:
#             tile_down = room.get_tile_down(self.position)
#             if tile_down is not None:
#                 current_tile = room.get_current_tile(self.position)
#                 current_tile.remove_pet()
#                 self.position['y'] += 1
#                 tile_down.add_pet()
#
#         elif move_direction == LEFT:
#             tile_left = room.get_tile_left(self.position)
#             if tile_left is not None:
#                 current_tile = room.get_current_tile(self.position)
#                 current_tile.remove_pet()
#                 self.position['x'] -= 1
#                 tile_left.add_pet()
#
#     def draw(self):
#         x = self.position['x'] * CELLSIZE
#         y = self.position['y'] * CELLSIZE
#         pet_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
#         pygame.draw.rect(DISPLAYSURF, PET, pet_rect)


if __name__ == '__main__':
    main()