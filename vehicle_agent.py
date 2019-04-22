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

        # Each successive move made by the car is drawn from this.  Initially, it's most likely that the car will
        # continue in the direction it's currently moving, but as it moves, that direction is removed from this list,
        # and eventually the car will turn.  At this point this variable will be reset, now favoring the new direction
        # self.possible_moves = []
        # self.setup_possible_moves_for_new_direction(self.direction)

        # self.path = dijkstra(self.position, self.destination)
        # self.path = dijsktra(self.city_map.intersections_graph, self.city_map.get_tile_at_position(self.position))
        self.path = self.get_path()

        self.turn_to_direction_map = {UP: self.go_up, RIGHT: self.go_right, DOWN: self.go_down, LEFT: self.go_left}

        self.body_color = car_body_color
        self.outline_color = car_outline_color
        self.dist_in_same_direction = 0

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

        # while (self.destination['x'], self.destination['y']) not in [(t.position['x'], t.position['y']) for t in path]:
        while destination_tile not in path:
            neighbors = self.city_map.get_adjacent_intersections(path[-1].position)
            current_tile = path[-1]
            closest_neighbor = None
            closest_neighbor_distance = math.inf
            for neighbor in neighbors:
                # if current_tile != path[-1]:

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
            if destination_tile not in path:
                path.append(closest_neighbor)

        return path

    # def get_path(self):
    #     graph = deepcopy(self.city_map.intersections_graph)
    #     current_tile = self.city_map.get_tile_at_position(self.position)
    #     adjacent_tiles = self.city_map.get_adjacent_intersections(self.position)
    #     for tile in adjacent_tiles:
    #         graph.add_edge(current_tile, tile, cost=distance(current_tile.position, tile.position), both_ends=True)
    #
    #     destination_tile = self.city_map.get_tile_at_position(self.destination)
    #     adjacent_tiles = self.city_map.get_adjacent_intersections(self.destination)
    #     for tile in adjacent_tiles:
    #         graph.add_edge(destination_tile, tile, cost=distance(destination_tile.position, tile.position), both_ends=True)
    #
    #     return graph.dijkstra(current_tile, self.city_map.get_tile_at_position(self.destination))

        # graph.add_node(current_tile)
        # adjacent_tiles = self.city_map.get_adjacent_intersections(self.position)
        # for tile in adjacent_tiles:
        #     graph.add_node(tile)
        #     graph.add_edge(current_tile, tile, distance(current_tile.position, tile.position))
        #     graph.add_edge(tile, current_tile, distance(current_tile.position, tile.position))
        #
        # dijsktra(graph, current_tile)

    # def plan_path_to_destination(self):
    #     best_path_moves = []
    #     best_path_length = math.inf
    #     unvisited_intersections = set(self.city_map.intersection_tiles)
    #
    #     # Keys will be each intersection and values will be distances to all the other adjacent intersections
    #     visited_intersections = {}
    #     # distances

    # def dijkstra_path(self, start_pos, finish_pos):
    #     if start_pos == finish_pos:
    #         return []
    #     unvisited_intersections = set(self.city_map.intersection_tiles)
    #     unvisited_intersections.discard(self.city_map.get_tile_at_position(start_pos))  # Remove start tile, if present
    #     # unvisited_intersections.add(self.city_map.get_tile_at_position(start_pos))
    #     unvisited_intersections.add(self.city_map.get_tile_at_position(finish_pos))
    #
    #     total_distances = {tile: math.inf for tile in unvisited_intersections}
    #     # total_distances[self.city_map.get_tile_at_position(start_pos)] = 0  # Starting tile has distance of 0
    #     previous_tiles = {tile: None for tile in unvisited_intersections}
    #
    #     while len(unvisited_intersections) > 0:
    #         curr_tile = list(sorted(total_distances.items(), key=lambda x: x[1]))[0][0]
    #         try:
    #             unvisited_intersections.remove(curr_tile)
    #         except KeyError:
    #             pass
    #
    #         for neighbor in self.city_map.get_adjacent_intersections(curr_tile.position):
    #             if neighbor not in unvisited_intersections:
    #                 continue
    #             dist = distance(curr_tile.position, neighbor.position) + total_distances[curr_tile]
    #             if dist < total_distances[neighbor]:
    #                 total_distances[neighbor] = dist
    #                 previous_tiles[neighbor] = curr_tile
    #
    #     shortest_path = []
    #     target = self.city_map.get_tile_at_position(finish_pos)
    #     if previous_tiles[target] is not None:
    #         while target is not None:
    #             shortest_path.insert(0, target)
    #             target = previous_tiles[target]
    #
    #     return shortest_path

    # def dijkstra_path(self, start_pos, finish_pos):
    #     visited = {self.city_map.get_tile_at_position(start_pos): 0}
    #     path = {}
    #
    #     nodes = set(self.city_map.intersection_tiles)
    #
    #     while nodes:
    #         min_node = None
    #         for node in nodes:
    #             if node in visited:
    #                 if min_node is None:
    #                     min_node = node
    #                 elif visited[node] < visited[min_node]:
    #                     min_node = node
    #
    #         if min_node is None:
    #             break
    #
    #         nodes.remove(min_node)
    #         current_weight = visited[min_node]
    #
    #         for edge in graph.edges[min_node]:
    #             weight = current_weight + graph.distance[(min_node, edge)]
    #             if edge not in visited or weight < visited[edge]:
    #                 visited[edge] = weight
    #                 path[edge] = min_node
    #
    # return visited, path

    # def estimate_shortest_path_length_from_a_to_b(self, start, finish):
    #     """Used as the heuristic function of the A* algorithm.  It needs some way to estimate the remaining distance to
    #     the finish line.
    #
    #     :param start:  Starting position
    #     :param finish: Finishing position
    #     :return:       Distance estimated from start to finish
    #     """
    #     # Since our imaginary city has perfectly rectilinear roads, the shortest possible distance betweeen any two
    #     # points should just be the sum of te vertical distance and the horizontal distance
    #     return abs(finish['x'] - start['x']) + abs(finish['y'] - start['y'])

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

    def setup_possible_moves_for_new_direction(self, direction):
        """Resets the queue of moves for the car after it changes directions.  It makes the car most likely to move in
        its current direction at first, but then as it works its way through the queue, it becomes more likely that
        it'll turn, and it is eventually guaranteed to turn at some point

        :param direction: The car's new direction
        """
        self.possible_moves = [direction] * MAX_DIST_WITHOUT_TURNING + \
                              [self.get_direction_to_right(direction)] + \
                              [self.get_direction_to_left(direction)]

        random.shuffle(self.possible_moves)

    def go_up(self):
        self.previous_position = deepcopy(self.position)
        if self.direction == UP:
            self.possible_moves.remove(UP)
        else:
            self.direction = UP
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['y'] -= 1

    def go_down(self):
        self.previous_position = deepcopy(self.position)
        if self.direction == DOWN:
            self.possible_moves.remove(DOWN)
        else:
            self.direction = DOWN
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['y'] += 1

    def go_right(self):
        self.previous_position = deepcopy(self.position)
        if self.direction == RIGHT:
            self.possible_moves.remove(RIGHT)
        else:
            self.direction = RIGHT
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['x'] += 1

    def go_left(self):
        self.previous_position = deepcopy(self.position)
        if self.direction == LEFT:
            self.possible_moves.remove(LEFT)
        else:
            self.direction = LEFT
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['x'] -= 1

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

    def can_move_to_tile(self, tile):
        """Checks that the tile can be moved onto

        :param tile: `Tile` object
        :return:     Bool, `True` if car can move onto tile, `False` otherwise
        """
        try:
            if tile in [self.get_tile_in_direction(direction, self.city_map) for direction in all_directions]:
                return tile.is_road and not tile.car
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
            elif self.path[0].position['y'] < self.position['y']:
                new_direction = DOWN
                # self.move_in_direction()
        # ...or maybe we're on the right row instead...
        elif self.path[0].position['y'] == self.position['y']:
            # If next waypoint is left...
            if self.path[0].position['x'] < self.position['x']:
                new_direction = LEFT
            # If next waypoint is right...
            elif self.path[0].position['x'] < self.position['x']:
                new_direction = RIGHT

        current_tile = city_map.get_current_tile(self.position)
        proposed_tile = self.get_tile_in_direction(new_direction, city_map)
        self.move_in_direction(new_direction, proposed_tile, current_tile)

        # for possible_move in self.possible_moves:
        #     proposed_tile = self.get_tile_in_direction(possible_move, city_map)
        #     if self.can_move_to_tile(proposed_tile):
        #         self.move_in_direction(possible_move, proposed_tile, city_map.get_current_tile(self.position))
        #         return
        #
        # # If we've made it here, then none of the possible moves in the list of possible moves was valid, meaning
        # # that the only valid move is to move backwards
        # self.move_in_direction(self.get_direction_backwards(self.direction),
        #                        self.get_tile_in_direction(self.get_direction_backwards(self.direction), city_map),
        #                        city_map.get_current_tile(self.position))

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
