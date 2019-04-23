import warnings, csv

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
        self.frames_waited_at_red_lights = 0
        self.velocity = 1

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
            current_tile = path[-1]
            neighbors = self.city_map.get_adjacent_intersections(current_tile.position)
            closest_neighbor = None
            closest_neighbor_distance = math.inf
            for neighbor in neighbors:
                if current_tile.position['y'] == self.destination['y'] or current_tile.position['x'] == \
                        self.destination['x']:
                    # If we're on the same row
                    if current_tile.position['y'] == self.destination['y']:
                        # And if the destination is between our current position and the next intersection over, go to it
                        if (current_tile.position['x'] < self.destination['x'] <= neighbor.position['x'] or
                                neighbor.position['x'] <= self.destination['x'] < current_tile.position['x']):
                            path.append(destination_tile)
                            break
                        # If the neighbor gets us closer, go to it
                        elif distance(neighbor.position, self.destination) < distance(current_tile.position,
                                                                                      self.destination):
                            path.append(neighbor)
                            break
                    if current_tile.position['x'] == self.destination['x']:
                        if (current_tile.position['y'] < self.destination['y'] <= neighbor.position['y'] or
                                neighbor.position['y'] <= self.destination['y'] < current_tile.position['y']):
                            path.append(destination_tile)
                            break
                        # If the neighbor gets us closer, go to it
                        elif distance(neighbor.position, self.destination) < distance(current_tile.position,
                                                                                      self.destination):
                            path.append(neighbor)
                            break

                elif distance(neighbor.position, self.destination) < closest_neighbor_distance:
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
        # for ii in range(self.velocity):
        # Don't run over any cars or blow through traffic lights
        if self.can_move_to_tile(next_tile):
            self.turn_to_direction_map[direction]()  # Adding the parentheses actually calls the method
            next_tile.add_car(self)
            previous_tile.remove_car(self)
            if self.destination == self.position:
                self.destination_reached = True
        else:  # if we didn't move, update previous position to be current position
            # TODO: change `self.go_up()` and other movement methods to not update `self.previous_position` so that we
            #       only do it once here
            self.previous_position = deepcopy(self.position)

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
                    if tile.light is None or tile.light.get_light_for_direction_of_travel(self.direction) != LightColor.red:
                        if not tile.car:
                            return True
                        # For simplicity, each tile represents a whole road (i.e., traffic in both directions)
                        elif tile.car.direction != self.direction:
                            return True
                    elif tile.light.get_light_for_direction_of_travel(self.direction) == LightColor.red:
                        self.frames_waited_at_red_lights += 1
                        # Only add one to the "waiting list" if the car just arrived; don't count subsequent iterations
                        if self.previous_position != self.position:
                            tile.light.add_car_waiting_on_light(self.direction)
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
        # Yes, I know we do this below, but we need to check it here as well.  I know it's ugly, but it works
        if self.position == self.path[0].position:
            self.path = self.path[1:]  # We've reached the next intersection, so we no longer need it as a waypoint
        elif self.position == self.destination:
            self.destination_reached = True
            return

        self.velocity = self.get_velocity()
        for ii in range(self.velocity):
            new_direction = self.direction  # Initialize `new_direction` so it's not `None` when we need to access it
            if self.position == self.path[0].position:
                self.path = self.path[1:]  # We've reached the next intersection, so we no longer need it as a waypoint
            elif self.position == self.destination:
                self.destination_reached = True
                return

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

    def get_velocity(self):
        if method != "flocking":
            return 1
        cars_ahead = self.get_cars_between_me_and_next_intersection()

        if len(cars_ahead) > 0:
            return 2  # Go slightly faster, but not excessively faster (there are still speed limits and stuff)
        else:
            return 1

    def get_cars_between_me_and_next_intersection(self):
        """Gets a list of cars between this car and the next intersection the car is approaching.  We only look at the
        cars straight ahead and cutoff the range at the nearest intersection straight ahead, because we don't want to
        start trying to flock to cars several blocks ahead.  And since cars will probably be going in a different
        direction after the intersection (and this car will turn rather than going straight over 50% of the time), we
        don't pay any attention to cars past the next intersection.

        :return: List of the cars which we can flock to
        """
        next_intersection_tile = self.path[0]

        tiles = self.city_map.get_tiles_between_tile_a_and_tile_b(self.city_map.get_tile_at_position(self.position),
                                                                  next_intersection_tile)

        cars = []
        for tile in tiles:
            if tile.car is not None:
                cars.append(tile.car)

        return cars

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

    def __del__(self):
        # warnings.warn("RE-ENABLE LOGGING!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print("DESTROYING CAR")
        self.position = None
        self.destination = None
        self.previous_position = None
        self.direction = None
        self.city_map = None
        self.path = None
        self.original_path = None

        self.turn_to_direction_map = None

        self.body_color = None
        self.outline_color = None
        self.destination_reached = None

        print(f"Frames spent waiting at red lights: {self.frames_waited_at_red_lights}")
        with open(logfile_name, 'a') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow([self.frames_waited_at_red_lights, method])
        self.frames_waited_at_red_lights = None

