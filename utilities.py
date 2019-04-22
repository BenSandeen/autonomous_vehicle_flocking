import math


def distance(start_pos, finish_pos):
    """Helper function to get the straight line distance between two locations

    :param start_pos:  Starting position
    :param finish_pos: Finishing position
    :return:           Distance between the two positions
    """
    return math.sqrt(pow(finish_pos['x'] - start_pos['x'], 2) + pow(finish_pos['y'] - start_pos['y'], 2))
