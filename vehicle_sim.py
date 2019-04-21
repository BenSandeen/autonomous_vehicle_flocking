# Final Project
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import sys
from vehicle_agent import Vehicle
from city_map import Map, make_map
from constants import *
from pygame.locals import *


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.display.set_caption('ALASKAN BULL WORMS!!!!!')

    show_start_screen()
    while True:
        run_game()


def run_game():
    city_map = make_map()

    # Set a random start point
    cars = []
    for i in range(NUM_CARS):
        cars.append(Vehicle(ORANGE, DARKORANGE, city_map))

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        for car in cars:
            car.move(city_map)

        DISPLAYSURF.fill(BGCOLOR)
        draw_grid(city_map)

        for car in cars:
            car.draw()

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


# def get_random_location():
#     return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def draw_grid(city_map):
    for tile_row in city_map.tiles:
        for tile in tile_row:
            x = tile.position['x'] * CELLSIZE
            y = tile.position['y'] * CELLSIZE

            tile_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, TILE, tile_rect)

            obstacle_or_dirt_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            if tile.is_road:
                pygame.draw.rect(DISPLAYSURF, FURNITURE, obstacle_or_dirt_rect)

            pygame.draw.rect(DISPLAYSURF, GRAY, tile_rect, 1)  # 1 is the width of the rectangles' outline


if __name__ == '__main__':
    main()
