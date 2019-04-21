import random, pygame
from constants import *


# For easily reasoning about turns
direction_to_left = {UP: LEFT, RIGHT: UP, DOWN: RIGHT, LEFT: DOWN}
direction_to_right = {UP: RIGHT, LEFT: UP, DOWN: LEFT, RIGHT: DOWN}
direction_backwards = {UP: DOWN, LEFT: RIGHT, DOWN: UP, RIGHT: LEFT}


class Vehicle:
    def __init__(self, roomba_body_color, roomba_outline_color, room): #, FPSCLOCK, DISPLAYSURF, BASICFONT):
        # self.FPSCLOCK = FPSCLOCK
        # self.DISPLAYSURF = DISPLAYSURF
        # self.BASICFONT = BASICFONT

        startx = random.randint(5, CELLWIDTH - 6)
        starty = random.randint(5, CELLHEIGHT - 6)

        self.position = {'x': startx, 'y': starty}

        while room.get_current_tile(self.position) is None:
            startx = random.randint(5, CELLWIDTH - 6)
            starty = random.randint(5, CELLHEIGHT - 6)

            self.position = {'x': startx, 'y': starty}

        self.direction = RIGHT

        # Each successive move made by the roomba is drawn from this.  Initially, it's most likely that the roomba will
        # continue in the direction it's currently moving, but as it moves, that direction is removed from this list,
        # and eventually the roomba will turn.  At this point this variable will be reset, now favoring the new
        # direction
        self.possible_moves = []
        self.setup_possible_moves_for_new_direction(self.direction)

        self.turn_to_direction_map = {UP: self.go_up, RIGHT: self.go_right, DOWN: self.go_down, LEFT: self.go_left}

        self.charger_location = [{'x': startx, 'y': starty}]
        self.body_color = roomba_body_color
        self.outline_color = roomba_outline_color
        self.dist_in_same_direction = 0

    def get_direction_to_left(self, direction):
        """Gets the direction to the left of the roomba, from the perspective of the direction that the roomba is
        facing.  E.g., if the roomba is facing UP, this will return LEFT, and if it's facing DOWN, this will return
        RIGHT

        :param direction: Which direction the roomba is currently facing
        :return:          Direction to the roomba's left-hand side
        """
        return direction_to_left[direction]

    def get_direction_to_right(self, direction):
        """Gets the direction to the right of the roomba, from the perspective of the direction that the roomba is
        facing.  E.g., if the roomba is facing UP, this will return RIGHT, and if it's facing DOWN, this will return
        LEFT

        :param direction: Which direction the roomba is currently facing
        :return:          Direction to the roomba's right-hand side
        """
        return direction_to_right[direction]

    def get_direction_backwards(self, direction):
        """Gets the direction opposite of the direction the roomba is currently facing.  E.g., if the roomba is facing
        UP, this will return DOWN, and if it's facing LEFT, this will return RIGHT

        :param direction: Which direction the roomba is currently facing
        :return:          Direction to the roomba's backside :P
        """
        return direction_backwards[direction]

    def setup_possible_moves_for_new_direction(self, direction):
        """Resets the queue of moves for the roomba after it changes directions.  It makes the roomba most likely to
        move in its current direction at first, but then as it works its way through the queue, it becomes more likely
        that it'll turn, and it is eventually guaranteed to turn at some point

        :param direction: The roomba's new direction
        """
        self.possible_moves = [direction] * MAX_DIST_WITHOUT_TURNING + \
                              [self.get_direction_to_right(direction)] + \
                              [self.get_direction_to_left(direction)]

        random.shuffle(self.possible_moves)

    def go_up(self):
        if self.direction == UP:
            self.possible_moves.remove(UP)
        else:
            self.direction = UP
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['y'] -= 1

    def go_down(self):
        if self.direction == DOWN:
            self.possible_moves.remove(DOWN)
        else:
            self.direction = DOWN
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['y'] += 1

    def go_right(self):
        if self.direction == RIGHT:
            self.possible_moves.remove(RIGHT)
        else:
            self.direction = RIGHT
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['x'] += 1

    def go_left(self):
        if self.direction == LEFT:
            self.possible_moves.remove(LEFT)
        else:
            self.direction = LEFT
            self.setup_possible_moves_for_new_direction(self.direction)
        self.position['x'] -= 1

    def move_in_direction(self, direction, next_tile, previous_tile):
        """Moves the Roomba in the desired direction.  When this method is called, the Roomba should already be certain
        that it can move to the tile in question.  This method also removes the roomba from the tile it is move away off
        of and onto the tile it is moving onto.

        :param direction:     Direction in which the roomba is moving
        :param next_tile:     `Tile` object onto which the roomba is moving
        :param previous_tile: `Tile` object off of which the roomba is moving
        """
        self.turn_to_direction_map[direction]()  # Adding the parentheses actually calls the method
        next_tile.add_roomba(self)
        previous_tile.remove_roomba(self)

    def can_move_to_tile(self, tile):
        """Checks that the tile can be moved onto

        :param tile: `Tile` object
        :return:     Bool, `True` if roomba can move onto tile, `False` otherwise
        """
        return tile is not None and not tile.drop and not tile.obstacle and not tile.pet and not tile.roomba

    def get_tile_in_direction(self, direction, room):
        if direction == UP:
            return room.get_tile_up(self.position)
        elif direction == RIGHT:
            return room.get_tile_right(self.position)
        elif direction == DOWN:
            return room.get_tile_down(self.position)
        elif direction == LEFT:
            return room.get_tile_left(self.position)

    def move(self, room):
        if room.get_current_tile(self.position).clean_dirt() <= 1:
            for possible_move in self.possible_moves:
                proposed_tile = self.get_tile_in_direction(possible_move, room)
                if self.can_move_to_tile(proposed_tile):
                    self.move_in_direction(possible_move, proposed_tile, room.get_current_tile(self.position))
                    return

            # If we've made it here, then none of the possible moves in the list of possible moves was valid, meaning
            # that the only valid move is to move backwards
            self.move_in_direction(self.get_direction_backwards(self.direction),
                                   self.get_tile_in_direction(self.get_direction_backwards(self.direction), room),
                                   room.get_current_tile(self.position))

        # If we've sucked up more than one unit of dirt, this tile is quite dirty, so instead of moving on, we stay for
        # an extra turn (eventually leaving once the tile is only slightly dirty (i.e., we suck up only one unit of dirt
        else:
            return

    def draw(self):
        x = self.position['x'] * CELLSIZE
        y = self.position['y'] * CELLSIZE
        roomba_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, self.outline_color, roomba_rect)
        roomba_inner_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, self.body_color, roomba_inner_rect)

    def explode(self):
        # print("BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!!!!!!")
        pass
