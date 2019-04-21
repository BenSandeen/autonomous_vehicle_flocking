import random, pygame, sys, math
from constants import *


class Map:
    def __init__(self, tiles):
        self.tiles = tiles

    def get_current_tile(self, position):
        """Gets tile at the current position

        :param position: Current position
        :return:         Tile the car is currently on top of
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

    def get_car_starting_tile(self):
        """Gets a tile where a car can reasonably start from

        :return: Tile on which a car may start
        """
        # return random.choice(filter(lambda x: not x.obstacle, self.tiles))
        try:
            poop = list(filter(lambda x: x.is_road, random.choice(self.tiles)))
            while not poop:
                poop = list(filter(lambda x: x.is_road, random.choice(self.tiles)))
            # return random.choice(list(filter(lambda x: x.is_road, random.choice(self.tiles)))).position
            return random.choice(poop).position
        except IndexError:
            pass


class Tile:
    def __init__(self, position, is_road):
        """Creates a `Tile` object, representing a square in the map of the room to be cleaned

        :param position:  Position of the tile
        :param is_road:   Bool, whether or not this tile is a road tile (and hence drivable or not)
        """
        # self.position = position
        # self.position = {'x': position['x'], 'y': position['y']}
        self._position = {'x': position['x'], 'y': position['y']}
        self.is_road = is_road
        self.car = None  # The car, if any, on the current tile

    @property
    def my_position(self):
        return self._position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_pos):
        pass


    # def is_dirty(self):
    #     return self.dirtiness > MIN_DIRTINESS
    #
    # def is_very_dirty(self):
    #     return self.dirtiness > MED_DIRTINESS
    #
    # def can_be_dirtier(self):
    #     return self.dirtiness < MAX_DIRTINESS
    #
    # def clean_dirt(self):
    #     """Removes dirt from tile.  If tile is quite dirty, it removes multiple dirt units at once
    #
    #     :return: Number of dirt units removed
    #     """
    #     if self.is_dirty():
    #         if self.is_very_dirty():
    #             self.dirtiness -= 2  # A lot of dirt got sucked up
    #             return 2
    #         else:
    #             self.dirtiness -= 1
    #             return 1
    #     return 0  # If there's no dirt on this tile, we can't clean anything from it
    #
    # def add_dirt(self):
    #     if self.can_be_dirtier():
    #         self.dirtiness += 1
    #
    # def add_obstacle(self):
    #     if not self.obstacle:
    #         self.obstacle = True
    #
    # def remove_obstacle(self):
    #     if self.obstacle:
    #         self.obstacle = False
    #
    # def add_pet(self):
    #     if not self.pet:
    #         self.pet = True
    #
    # def remove_pet(self):
    #     if self.pet:
    #         self.pet = False

    def add_car(self, car):
        if self.car is not None:
            car.explode()
        self.car = car

    def remove_car(self, car):
        if self.car != car:
            # Note from car owner's manual: If your car explodes upon startup, this is not unexpected behavior.
            # Please continue to enjoy your car!
            car.explode()
        self.car = None

    # def add_drop(self):
    #     if not self.drop:
    #         self.drop = True


def make_map():
    """Makes a city map

    :return: `Map` object, consisting of a bunch of tiles
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

            # # make room irregularly shaped by omitting tiles
            # if y == 6 and x < 6:
            #     tiles[row_idx].append(None)
            #     continue
            # elif y == 11 and x > (WINDOWWIDTH / CELLSIZE) - 4:
            #     tiles[row_idx].append(None)
            #     continue
            #
            # # Make big rectangular gap in middle of room
            # elif 3 * CELLWIDTH / 7 < col_idx < 4 * CELLWIDTH / 7 and 3 * CELLHEIGHT / 7 < row_idx < 4 * CELLHEIGHT / 7:
            #     tiles[row_idx].append(None)
            #     continue

            # Make buffer around map so that cars don't attempt to drive off the edge
            if y == 0 or x == 0 or y == CELLHEIGHT - 1 or x == CELLWIDTH - 1:
                tiles[row_idx].append(Tile(position={'x': x, 'y': y}, is_road=False))
                continue

            # Make roads all along the edge of the map (actually, one tile in from the edge)
            elif y == 1 or x == 1 or y == CELLHEIGHT - 2 or x == CELLWIDTH - 2:
                tiles[row_idx].append(Tile(position={'x': x, 'y': y}, is_road=True))
                continue

            elif y % 24 == 0 or x % 24 == 0:
                tiles[row_idx].append(Tile(position={'x': x, 'y': y}, is_road=True))
                continue

            # dirt_level = random.randint(MIN_DIRTINESS, MAX_DIRTINESS)

            # We'll handle the `drop` and `obstacle` stuff later, because we don't want to have too many drops or
            # obstacles that the cars can't move
            # tile = Tile(position={'x': x, 'y': y}, dirtiness=dirt_level, drop=False, obstacle=False, pet=False)
            else:
                tile = Tile(position={'x': x, 'y': y}, is_road=False)
                tiles[row_idx].append(tile)

    # for obstacle in range(NUM_OBSTACLES):
    #     tile_col = random.randint(0, max_y)
    #     tile_row = random.randint(0, max_x)
    #     if tiles[tile_col][tile_row] is not None:
    #         tiles[tile_col][tile_row].add_obstacle()

    room = Map(tiles)

    return room
