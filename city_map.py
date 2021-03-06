import random
from copy import deepcopy

from constants import *
from utilities import *
from traffic_light import *


class Map:
    def __init__(self, tiles):
        self.tiles = tiles
        self.traffic_lights = []
        self.intersection_tiles = self.get_intersection_tiles()
    #     self.intersections_graph = self.create_intersections_graph()
    #
    # def create_intersections_graph(self):
    #     graph = Graph([])
    #     for intersection in self.intersection_tiles:
    #         # graph.add_node(intersection)
    #         for neighbor in self.get_adjacent_intersections(intersection.position):
    #             # graph.add_node(neighbor)
    #             # graph.add_edge(intersection, neighbor, distance(intersection.position, neighbor.position))
    #             graph.add_edge(intersection, neighbor, cost=distance(intersection.position, neighbor.position),
    #                            both_ends=True)
    #
    #             # # Since our graph is undirected, we need to add the edge going in the opposite direction
    #             # graph.add_edge(neighbor, intersection, distance(intersection.position, neighbor.position))
    #
    #     return graph

    def update_traffic_lights(self):
        for tile in self.intersection_tiles:
            tile.light.change_lights_possibly()

    def get_intersection_tiles(self):
        """Gets all tiles located at intersections.  This is important for pathfinding and placing street lights

        :return: List of all tiles located at intersections
        """
        intersection_tiles = []
        for tile in filter(lambda x: x.is_road, self.get_flat_list_of_tiles()):
            tile_up = self.get_tile_up(tile.position)
            tile_down = self.get_tile_down(tile.position)
            tile_left = self.get_tile_left(tile.position)
            tile_right = self.get_tile_right(tile.position)

            if (tile_up.is_road or tile_down.is_road) and (tile_left.is_road or tile_right.is_road):
                tile.light = TrafficLight(tile.position)
                self.traffic_lights.append(tile.light)
                intersection_tiles.append(tile)

        return intersection_tiles

    def draw_lights(self):
        for light in self.traffic_lights:
            light.draw()

    def get_tile_at_position(self, position):
        return [t for t in self.get_flat_list_of_tiles() if
                t.position['x'] == position['x'] and t.position['y'] == position['y']][0]

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

    def get_random_road_tile_position(self):
        """Gets a tile where a car can reasonably start from

        :return: Tile on which a car may start
        """
        try:
            random_row = list(filter(lambda x: x.is_road, random.choice(self.tiles)))
            while not random_row:
                random_row = list(filter(lambda x: x.is_road, random.choice(self.tiles)))
            starting_tile = random.choice(random_row)
            # return {'x': starting_tile.position['x'], 'y': starting_tile.position['y']}
            return deepcopy(starting_tile.position)
        except IndexError:
            pass

    def get_nearest_intersections_positions(self, position, excluded_intersections=[]):
        closest_intersection_dist = math.inf
        closest_intersection = None
        for tile in self.intersection_tiles:
            dist = distance(tile.position, position)
            if dist <= closest_intersection_dist and tile not in excluded_intersections:
                closest_intersection = tile
                closest_intersection_dist = dist

        return deepcopy(closest_intersection.position)

    def get_adjacent_intersections(self, position):
        """Assumes `position` is the position of an intersection tile.  Gets all adjacent intersection tiles

        :param position: Current intersection tile's position
        :return:         All adjacent intersection tiles
        """
        adjacent_tiles = []

        # If we're not at an intersection, just get the two intersections at end of the which block we're on
        if (position['x'], position['y']) not in [(tile.position['x'], tile.position['y']) for tile in
                                                  self.intersection_tiles]:
            # adjacent_tiles.append(self.get_tile_at_position(self.get_nearest_intersections_positions(position)))
            # adjacent_tiles.append(self.get_tile_at_position(
            #     self.get_nearest_intersections_positions(position, excluded_intersections=[adjacent_tiles[0]])))

            if position['x'] in [t.position['x'] for t in self.intersection_tiles]:
                adjacent_tiles.append(self.get_intersection_up(position))
                adjacent_tiles.append(self.get_intersection_down(position))
            elif position['y'] in [t.position['y'] for t in self.intersection_tiles]:
                adjacent_tiles.append(self.get_intersection_left(position))
                adjacent_tiles.append(self.get_intersection_right(position))

            return adjacent_tiles

        # Check nearest four intersection tiles, because our intersections can only have a maximum of four neighbors
        # (one up, one down, one left, and one right)
        nearest_intersections = list(sorted(self.intersection_tiles, key=lambda x: distance(position, x.position)))
        nearest_intersections.remove(self.get_tile_at_position(position))  # Don't include tile we're currently at
        for tile in nearest_intersections[:4]:
            if tile.position['x'] == position['x']:
                if tile.position['x'] not in [t.position['x'] for t in adjacent_tiles]:
                    adjacent_tiles.append(tile)
                # If there's a tile in the same column (x increments across the columns, remember), then make sure it's
                # on the other side of the tile whose neighbors we want to find.  This prevents, for example, the upper
                # left corner tile from returning both the intersection immediately below it and the intersection below
                # that as its neighbors
                else:
                    other_tile_y = [t.position['y'] for t in adjacent_tiles if t.position['x'] == tile.position['x']][0]

                    # Make sure the central tile is between the existing neighbor and the potential one
                    if tile.position['y'] < position['y'] < other_tile_y or other_tile_y < position['y'] < \
                            tile.position['y']:
                        adjacent_tiles.append(tile)
            elif tile.position['y'] == position['y']:
                if tile.position['y'] not in [t.position['y'] for t in adjacent_tiles]:
                    adjacent_tiles.append(tile)
                else:
                    other_tile_x = [t.position['x'] for t in adjacent_tiles if t.position['y'] == tile.position['y']][0]

                    if tile.position['x'] < position['x'] < other_tile_x or other_tile_x < position['x'] < \
                            tile.position['x']:
                        adjacent_tiles.append(tile)

        return adjacent_tiles

    def get_intersection_up(self, position):
        """Assumes position is in a road going up and down

        :param position:
        :return:
        """
        for tile in [t for t in self.intersection_tiles if t.position['x'] == position['x']]:
            if position['y'] - BLOCKLENGTH <= tile.position['y'] <= position['y']:
                return tile

        raise ValueError(f"Couldn't find intersection up")

    def get_intersection_down(self, position):
        """Assumes position is in a road going up and down

        :param position:
        :return:
        """
        for tile in [t for t in self.intersection_tiles if t.position['x'] == position['x']]:
            if position['y'] <= tile.position['y'] <= position['y'] + BLOCKLENGTH:
                return tile

        raise ValueError(f"Couldn't find intersection up")

    def get_intersection_left(self, position):
        """Assumes position is in a road going left and right

        :param position:
        :return:
        """
        for tile in [t for t in self.intersection_tiles if t.position['y'] == position['y']]:
            if position['x'] - BLOCKLENGTH <= tile.position['x'] <= position['x']:
                return tile

        raise ValueError(f"Couldn't find intersection up")

    def get_intersection_right(self, position):
        """Assumes position is in a road going left and right

        :param position:
        :return:
        """
        for tile in [t for t in self.intersection_tiles if t.position['y'] == position['y']]:
            if position['x'] <= tile.position['x'] <= position['x'] + BLOCKLENGTH:
                return tile

        raise ValueError(f"Couldn't find intersection up")

    def get_tiles_between_tile_a_and_tile_b(self, tile_a, tile_b):
        """Gets list of tiles between `tile_a` and `tile_b`.  These tiles must be in either the same column or row, and
        must only be connected by tiles in the same column or row, respectively (i.e., we don't want to count tiles in
        the same column but which are in the middle of left-to-right blocks; basically, we want a path that a car can
        drive without moving to a different column or row, respectively)

        :param tile_a: Starting tile (exclusive)
        :param tile_b: Finishing tile (inclusive)
        :return:       List of the tiles in the range
        """
        if tile_a.position['x'] != tile_b.position['x'] and tile_a.position['y'] != tile_b.position['y']:
            raise ValueError(f"Tiles must be in either the same column or the same row!")

        tiles = []

        # We can use the intersections to check whether the tiles can be connected by a straight line of road tiles
        if tile_a.position['x'] == tile_b.position['x']:
            if tile_a.position['x'] not in [t.position['x'] for t in self.intersection_tiles]:
                raise ValueError(f"Tiles must be connected by a road in the same column!")
            if tile_a.position['y'] > tile_b.position['y']:
                next_tile_method = self.get_tile_up
            elif tile_a.position['y'] < tile_b.position['y']:
                next_tile_method = self.get_tile_down
            else:
                raise ValueError(f"Tiles shouldn't be the same!")

            tiles.append(self.get_tile_at_position(next_tile_method(tile_a.position).position))

            while tile_b not in tiles:
                tiles.append(self.get_tile_at_position(next_tile_method(tiles[-1].position).position))

        if tile_a.position['y'] == tile_b.position['y']:
            if tile_a.position['y'] not in [t.position['y'] for t in self.intersection_tiles]:
                raise ValueError(f"Tiles must be connected by a road in the same row!")
            if tile_a.position['x'] > tile_b.position['x']:
                next_tile_method = self.get_tile_left
            elif tile_a.position['x'] < tile_b.position['x']:
                next_tile_method = self.get_tile_right
            else:
                raise ValueError(f"Tiles shouldn't be the same!")

            tiles.append(self.get_tile_at_position(next_tile_method(tile_a.position).position))

            while tile_b not in tiles:
                tiles.append(self.get_tile_at_position(next_tile_method(tiles[-1].position).position))

        return tiles

    def get_flat_list_of_tiles(self):
        tiles = []
        for row in self.tiles:
            for tile in row:
                tiles.append(tile)
        return tiles


class Tile:
    def __init__(self, position, is_road):
        """Creates a `Tile` object, representing a square in the map of the city

        :param position: Position of the tile
        :param is_road:  Bool, whether or not this tile is a road tile (and hence drivable or not)
        """
        self.position = deepcopy(position)
        self.is_road = is_road
        self.car = None  # The car, if any, on the current tile
        self.light = None

    def add_car(self, car):
        # if self.car is not None:
        #     car.explode()
        self.car = car

    def remove_car(self, car):
        # if self.car != car:
        #     # Note from car owner's manual: If your car explodes upon startup, this is not unexpected behavior.
        #     # Please continue to enjoy your car!
        #     car.explode()
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

            elif y % BLOCKLENGTH == 0 or x % BLOCKLENGTH == 0:
                tiles[row_idx].append(Tile(position={'x': x, 'y': y}, is_road=True))
                continue

            # We'll handle the `drop` and `obstacle` stuff later, because we don't want to have too many drops or
            # obstacles that the cars can't move
            else:
                tile = Tile(position={'x': x, 'y': y}, is_road=False)
                tiles[row_idx].append(tile)

    city_map = Map(tiles)

    return city_map
