import random, pygame, sys, math
from constants import *


class Map:
    def __init__(self, tiles):
        self.tiles = tiles

    def get_current_tile(self, position):
        """Gets tile at the current position

        :param position: Current position
        :return:         Tile the roomba is currently on top of
        """
        return self.tiles[position['y']][position['x']]

    def get_tile_up(self, position):
        """Gets tile one tile up from current position

        :param position: Current position
        :return:         If there's a tile up from current tile, return that, otherwise return `None`
        """
        if position['y'] <= 0:
            return None
        return self.tiles[position['y'] - 1][position['x']]

    def get_tile_down(self, position):
        """Gets tile one tile down from current position

        :param position: Current position
        :return:         If there's a tile down from current tile, return that, otherwise return `None`
        """
        if position['y'] >= CELLHEIGHT - 1:
            return None
        return self.tiles[position['y'] + 1][position['x']]

    def get_tile_left(self, position):
        """Gets tile one tile left from current position

        :param position: Current position
        :return:         If there's a tile left from current tile, return that, otherwise return `None`
        """
        if position['x'] <= 0:
            return None
        return self.tiles[position['y']][position['x'] - 1]

    def get_tile_right(self, position):
        """Gets tile one tile right from current position

        :param position: Current position
        :return:         If there's a tile right from current tile, return that, otherwise return `None`
        """
        if position['x'] >= CELLWIDTH - 1:
            return None
        return self.tiles[position['y']][position['x'] + 1]


class Tile:
    def __init__(self, position, dirtiness, drop, obstacle, pet):
        """Creates a `Tile` object, representing a square in the map of the room to be cleaned

        :param position:  Position of the tile
        :param dirtiness: Level of dirtiness of the tile; comes in integer gradations, 0 being clean and higher numbers
                          being successively more dirty
        :param drop:      Bool, whether or not there's a dropoff in elevation for this tile
        :param obstacle:  Bool, whether or not this tile has an obstacle in it
        :param pet:       Bool, whether or not this tile has a pet in it
        """
        self.position = position
        self.dirtiness = dirtiness
        self.drop = drop
        self.obstacle = obstacle
        self.pet = pet
        self.roomba = None

    def is_dirty(self):
        return self.dirtiness > MIN_DIRTINESS

    def is_very_dirty(self):
        return self.dirtiness > MED_DIRTINESS

    def can_be_dirtier(self):
        return self.dirtiness < MAX_DIRTINESS

    def clean_dirt(self):
        """Removes dirt from tile.  If tile is quite dirty, it removes multiple dirt units at once

        :return: Number of dirt units removed
        """
        if self.is_dirty():
            if self.is_very_dirty():
                self.dirtiness -= 2  # A lot of dirt got sucked up
                return 2
            else:
                self.dirtiness -= 1
                return 1
        return 0  # If there's no dirt on this tile, we can't clean anything from it

    def add_dirt(self):
        if self.can_be_dirtier():
            self.dirtiness += 1

    def add_obstacle(self):
        if not self.obstacle:
            self.obstacle = True

    def remove_obstacle(self):
        if self.obstacle:
            self.obstacle = False

    def add_pet(self):
        if not self.pet:
            self.pet = True

    def remove_pet(self):
        if self.pet:
            self.pet = False

    def add_roomba(self, roomba):
        if self.roomba is not None:
            roomba.explode()
        self.roomba = roomba

    def remove_roomba(self, roomba):
        if self.roomba != roomba:
            # Note from Roomba owner's manual: If your Roomba explodes upon startup, this is not unexpected behavior.
            # Please continue to enjoy your Roomba!
            roomba.explode()
        self.roomba = None

    def add_drop(self):
        if not self.drop:
            self.drop = True


def make_map():
    """Makes a room object that satisfies all the requirements

    :return: `Room` object, consisting of a bunch of tiles
    """
    tiles = []
    max_x = 0
    max_y = 0
    for row_idx, y in enumerate(range(0, CELLHEIGHT)):
        # Add a list for the new row
        tiles.append([])
        if row_idx > max_y:
            max_y = row_idx

        for col_idx, x in enumerate(range(0, CELLWIDTH)):
            if col_idx > max_x:
                max_x = col_idx

            # make room irregularly shaped by omitting tiles
            if y == 6 and x < 6:
                tiles[row_idx].append(None)
                continue
            elif y == 11 and x > (WINDOWWIDTH / CELLSIZE) - 4:
                tiles[row_idx].append(None)
                continue

            # Make big rectangular gap in middle of room
            elif 3 * CELLWIDTH / 7 < col_idx < 4 * CELLWIDTH / 7 and 3 * CELLHEIGHT / 7 < row_idx < 4 * CELLHEIGHT / 7:
                tiles[row_idx].append(None)
                continue

            dirt_level = random.randint(MIN_DIRTINESS, MAX_DIRTINESS)

            # We'll handle the `drop` and `obstacle` stuff later, because we don't want to have too many drops or
            # obstacles that the roombas can't move
            tile = Tile(position={'x': x, 'y': y}, dirtiness=dirt_level, drop=False, obstacle=False, pet=False)
            tiles[row_idx].append(tile)

    for obstacle in range(NUM_OBSTACLES):
        tile_col = random.randint(0, max_y)
        tile_row = random.randint(0, max_x)
        if tiles[tile_col][tile_row] is not None:
            tiles[tile_col][tile_row].add_obstacle()

    # for pet in range(NUM_PETS):
    #     tile_col = random.randint(0, max_y)
    #     tile_row = random.randint(0, max_x)
    #     if tiles[tile_col][tile_row] is not None:
    #         tiles[tile_col][tile_row].add_pet()

    for drop in range(NUM_DROPS):
        tile_col = random.randint(0, max_y)
        tile_row = random.randint(0, max_x)
        if tiles[tile_col][tile_row] is not None:
            tiles[tile_col][tile_row].add_drop()

    room = Map(tiles)

    return room
