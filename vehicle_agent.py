from city_map import *

all_directions = [UP, DOWN, LEFT, RIGHT]
# For easily reasoning about turns
direction_to_left = {UP: LEFT, RIGHT: UP, DOWN: RIGHT, LEFT: DOWN}
direction_to_right = {UP: RIGHT, LEFT: UP, DOWN: LEFT, RIGHT: DOWN}
direction_backwards = {UP: DOWN, LEFT: RIGHT, DOWN: UP, RIGHT: LEFT}


class Vehicle:
    def __init__(self, car_body_color, car_outline_color, city_map):
        self.position = city_map.get_random_road_tile_position()
        self.destination = city_map.get_random_road_tile_position()
        self.previous_position = None
        self.direction = RIGHT
        self.city_map = city_map  # Used for reasoning about navigation
        self.path = self.get_path()
        self.original_path = deepcopy(self.path)

        self.turn_to_direction_map = {UP: self.go_up, RIGHT: self.go_right, DOWN: self.go_down, LEFT: self.go_left}

        self.body_color = car_body_color
        self.outline_color = car_outline_color
        self.destination_reached = False

    def get_path(self):
        """This is ugly and unsophisticated, but it gets the cars to their goals.  Besides, the point of my project is
        not to implement an efficient path-finding algorithm, it's to augment autonomous vehicles to be more cooperative

        :return: The series of intersections to travel through to reach the car's destination
        """
        path = [self.city_map.get_tile_at_position(self.position)]
        destination_tile = self.city_map.get_tile_at_position(self.destination)

        neighbors = self.city_map.get_adjacent_intersections(self.position)
        closest_neighbor = None
        closest_neighbor_distance = math.inf
        for neighbor in neighbors:
            if distance(neighbor.position, self.position) < closest_neighbor_distance:
                closest_neighbor = neighbor
                closest_neighbor_distance = distance(neighbor.position, self.position)

        path.append(closest_neighbor)

        while destination_tile not in path:
            neighbors = self.city_map.get_adjacent_intersections(path[-1].position)
            current_tile = path[-1]
            closest_neighbor = None
            closest_neighbor_distance = math.inf
            for neighbor in neighbors:
                # If we're on the same row
                if current_tile.position['y'] == self.destination['y']:
                    # And if the destination is between our current position and the next intersection over, go to it
                    if (current_tile.position['x'] < self.destination['x'] < neighbor.position['x'] or
                            neighbor.position['x'] < self.destination['x'] < current_tile.position['x']):
                        path.append(destination_tile)
                        break
                    # If the neighbor gets us closer, go to it
                    elif distance(neighbor.position, self.destination) < distance(current_tile.position, self.destination):
                        path.append(neighbor)
                        break
                if current_tile.position['x'] == self.destination['x']:
                    if (current_tile.position['y'] < self.destination['y'] < neighbor.position['y'] or
                            neighbor.position['y'] < self.destination['y'] < current_tile.position['y']):
                        path.append(destination_tile)
                        break
                    # If the neighbor gets us closer, go to it
                    elif distance(neighbor.position, self.destination) < distance(current_tile.position, self.destination):
                        path.append(neighbor)
                        break

                if distance(neighbor.position, self.destination) < closest_neighbor_distance:
                    closest_neighbor = neighbor
                    closest_neighbor_distance = distance(neighbor.position, self.destination)

            # If the last iteration through the loop did reach the destination, don't append this
            if destination_tile not in path and closest_neighbor is not None:
                path.append(closest_neighbor)

        return path

    def get_direction_to_left(self, direction):
        """Gets the direction to the left of the car, from the perspective of the direction that the car is facing.
        E.g., if the car is facing UP, this will return LEFT, and if it's facing DOWN, this will return RIGHT

        :param direction: Which direction the car is currently facing
        :return:          Direction to the car's left-hand side
        """
        return direction_to_left[direction]

    def get_direction_to_right(self, direction):
        """Gets the direction to the right of the car, from the perspective of the direction that the car is facing.
        E.g., if the car is facing UP, this will return RIGHT, and if it's facing DOWN, this will return LEFT

        :param direction: Which direction the car is currently facing
        :return:          Direction to the car's right-hand side
        """
        return direction_to_right[direction]

    def get_direction_backwards(self, direction):
        """Gets the direction opposite of the direction the car is currently facing.  E.g., if the car is facing UP,
        this will return DOWN, and if it's facing LEFT, this will return RIGHT

        :param direction: Which direction the car is currently facing
        :return:          Direction to the car's backside :P
        """
        return direction_backwards[direction]

    def go_up(self):
        self.previous_position = deepcopy(self.position)
        # self.position['y'] -= 1
        self.direction = UP
        self.position = {'x': self.position['x'], 'y': self.position['y'] - 1}

    def go_down(self):
        self.previous_position = deepcopy(self.position)
        # self.position['y'] += 1
        self.direction = DOWN
        self.position = {'x': self.position['x'], 'y': self.position['y'] + 1}

    def go_right(self):
        self.previous_position = deepcopy(self.position)
        # self.position['x'] += 1
        self.direction = RIGHT
        self.position = {'x': self.position['x'] + 1, 'y': self.position['y']}

    def go_left(self):
        self.previous_position = deepcopy(self.position)
        # self.position['x'] -= 1
        self.direction = LEFT
        self.position = {'x': self.position['x'] - 1, 'y': self.position['y']}

    def move_in_direction(self, direction, next_tile, previous_tile):
        """Moves the car in the desired direction.  When this method is called, the car should already be certain that
        it can move to the tile in question.  This method also removes the car from the tile it is move away off of and
        onto the tile it is moving onto.

        :param direction:     Direction in which the car is moving
        :param next_tile:     `Tile` object onto which the car is moving
        :param previous_tile: `Tile` object off of which the car is moving
        """
        # Don't run over any cars or blow through traffic lights
        if self.can_move_to_tile(next_tile):
            self.turn_to_direction_map[direction]()  # Adding the parentheses actually calls the method
            next_tile.add_car(self)
            previous_tile.remove_car(self)
            if self.destination == self.position:
                self.destination_reached = True

    def destroy(self):
        """To be called by the main simulator when the car reaches its destination.  It removes the car from the tile
        objects so that other cars can continue on their way
        """
        self.city_map.get_tile_at_position(self.position).car = None

    def can_move_to_tile(self, tile):
        """Checks that the tile can be moved onto

        :param tile: `Tile` object
        :return:     Bool, `True` if car can move onto tile, `False` otherwise
        """
        try:
            if tile in [self.get_tile_in_direction(direction, self.city_map) for direction in all_directions]:
                if tile.is_road:
                    if not tile.car:
                        return True
                    elif tile.car.direction != self.direction:
                        return True
            return False
        except AttributeError:
            pass

    def get_tile_in_direction(self, direction, city_map):
        if direction == UP:
            return city_map.get_tile_up(self.position)
        elif direction == RIGHT:
            return city_map.get_tile_right(self.position)
        elif direction == DOWN:
            return city_map.get_tile_down(self.position)
        elif direction == LEFT:
            return city_map.get_tile_left(self.position)

    def move(self, city_map):
        new_direction = self.direction
        if self.position == self.path[0].position:
            self.path = self.path[1:]  # We've reached the next intersection, so we no longer need it as a waypoint

        # If we're on the right column for the next waypoint...
        if self.path[0].position['x'] == self.position['x']:
            # If next waypoint is up...
            if self.path[0].position['y'] < self.position['y']:
                new_direction = UP
            # If next waypoint is down...
            elif self.position['y'] < self.path[0].position['y']:
                new_direction = DOWN

        # ...or maybe we're on the right row instead...
        elif self.path[0].position['y'] == self.position['y']:
            # If next waypoint is left...
            if self.path[0].position['x'] < self.position['x']:
                new_direction = LEFT
            # If next waypoint is right...
            elif self.position['x'] < self.path[0].position['x']:
                new_direction = RIGHT

        current_tile = city_map.get_current_tile(self.position)
        proposed_tile = self.get_tile_in_direction(new_direction, city_map)
        self.move_in_direction(new_direction, proposed_tile, current_tile)

    def draw(self):
        x = self.position['x'] * CELLSIZE
        y = self.position['y'] * CELLSIZE
        car_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, self.outline_color, car_rect)
        # car_inner_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        # pygame.draw.rect(DISPLAYSURF, self.body_color, car_inner_rect)

    def explode(self):
        # print("BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!!!!!!")
        pass
