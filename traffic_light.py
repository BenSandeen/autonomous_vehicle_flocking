from constants import *
import enum
import random, math
from copy import deepcopy


class LightColor(enum.Enum):
    green = 'green'
    yellow = 'yellow'
    red = 'red'


class TrafficLight:
    def __init__(self, position):
        """These directions represent the color for a car travelling in the given direction.  E.g., a car travelling
        right would look at `self.right`
        """
        self.up = LightColor.green
        self.down = LightColor.green
        self.left = LightColor.red
        self.right = LightColor.red

        self.position = deepcopy(position)

        self.yellow_duration = 6

        # Since lights facing in opposite directions should always change together, we use a single timer for each pair
        self.up_and_down_time_until_light_change = random.randint(20, 30)
        self.left_and_right_time_until_light_change = math.inf

    def get_rgb_color_value(self, light_color):
        if light_color == LightColor.green:
            return GREEN
        elif light_color == LightColor.yellow:
            return YELLOW
        elif light_color == LightColor.red:
            return RED

    def get_light_for_direction_of_travel(self, direction):
        if direction == UP:
            return self.up
        elif direction == DOWN:
            return self.down
        elif direction == LEFT:
            return self.left
        elif direction == RIGHT:
            return self.right

    def change_lights_possibly(self):
        """Handles changing the lights.  Doesn't actually change until this method has been called a certain number of
        times, for simplicity.  This way we can just have the main loop call into this every iteration and this will
        handle how frequently to change the lights
        """
        if self.up_and_down_time_until_light_change != 0:
            self.up_and_down_time_until_light_change -= 1
        else:
            self.up = self.get_next_light_color(self.up)
            self.down = self.get_next_light_color(self.down)
            assert self.up == self.down

            # If the lights turned red, then turn the other lights green
            if self.up == LightColor.red:
                self.left = self.get_next_light_color(self.left)
                self.right = self.get_next_light_color(self.right)
                assert self.left == self.right

                self.left_and_right_time_until_light_change = self.get_light_duration(self.left)

            self.up_and_down_time_until_light_change = self.get_light_duration(self.up)

            return

        if self.left_and_right_time_until_light_change != 0:
            self.left_and_right_time_until_light_change -= 1
        else:
            self.left = self.get_next_light_color(self.left)
            self.right = self.get_next_light_color(self.right)
            assert self.left == self.right

            # If the lights turned red, then turn the other lights green
            if self.left == LightColor.red:
                self.up = self.get_next_light_color(self.up)
                self.down = self.get_next_light_color(self.down)
                assert self.up == self.down

                self.up_and_down_time_until_light_change = self.get_light_duration(self.up)

            self.left_and_right_time_until_light_change = self.get_light_duration(self.left)

            return

    def get_next_light_color(self, light_color):
        if light_color == LightColor.green:
            return LightColor.yellow
        elif light_color == LightColor.yellow:
            return LightColor.red
        elif light_color == LightColor.red:
            return LightColor.green

    def get_light_duration(self, light_color):
        if light_color == LightColor.green:
            return random.randint(20, 30)
        elif light_color == LightColor.yellow:
            return self.yellow_duration
        # Red lights wait on lights in other direction to become red before changing
        elif light_color == LightColor.red:
            return math.inf

    def draw(self):
        x = self.position['x'] * CELLSIZE
        y = self.position['y'] * CELLSIZE
        car_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

        top_left     = (self.position['x'] * CELLSIZE,                  self.position['y'] * CELLSIZE)
        top_right    = (self.position['x'] * CELLSIZE + CELLSIZE,       self.position['y'] * CELLSIZE)
        bottom_left  = (self.position['x'] * CELLSIZE,                  self.position['y'] * CELLSIZE + CELLSIZE)
        bottom_right = (self.position['x'] * CELLSIZE + CELLSIZE,       self.position['y'] * CELLSIZE + CELLSIZE)
        center       = (self.position['x'] * CELLSIZE + 0.5 * CELLSIZE, self.position['y'] * CELLSIZE + 0.5 * CELLSIZE)

        # Light for traffic heading up...
        pygame.draw.polygon(DISPLAYSURF, self.get_rgb_color_value(self.up), [bottom_left, center, bottom_right])

        # ...for traffic heading down...
        pygame.draw.polygon(DISPLAYSURF, self.get_rgb_color_value(self.down), [top_left, top_right, center])

        # ...for traffic heading left...
        pygame.draw.polygon(DISPLAYSURF, self.get_rgb_color_value(self.left), [center, top_right, bottom_right])

        # ...for traffic heading right...
        pygame.draw.polygon(DISPLAYSURF, self.get_rgb_color_value(self.right), [bottom_left, top_left, center])
