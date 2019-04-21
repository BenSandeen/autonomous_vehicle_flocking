import random
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

    def get_car_starting_tile_position(self):
        """Gets a tile where a car can reasonably start from

        :return: Tile on which a car may start
        """
        try:
            random_row = list(filter(lambda x: x.is_road, random.choice(self.tiles)))
            while not random_row:
                random_row = list(filter(lambda x: x.is_road, random.choice(self.tiles)))
            starting_tile = random.choice(random_row)
            return {'x': starting_tile.position['x'], 'y': starting_tile.position['y']}
        except IndexError:
            pass


class Tile:
    def __init__(self, position, is_road):
        """Creates a `Tile` object, representing a square in the map of the city

        :param position: Position of the tile
        :param is_road:  Bool, whether or not this tile is a road tile (and hence drivable or not)
        """
        self.position = {'x': position['x'], 'y': position['y']}
        self.is_road = is_road
        self.car = None  # The car, if any, on the current tile

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

            # We'll handle the `drop` and `obstacle` stuff later, because we don't want to have too many drops or
            # obstacles that the cars can't move
            # tile = Tile(position={'x': x, 'y': y}, dirtiness=dirt_level, drop=False, obstacle=False, pet=False)
            else:
                tile = Tile(position={'x': x, 'y': y}, is_road=False)
                tiles[row_idx].append(tile)

    city_map = Map(tiles)

    return city_map
