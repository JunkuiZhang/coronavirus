import setting
import math
from random import gauss
from pygame.math import Vector2


def dist_cal(pos1, pos2):
    x_square = (pos1[0] - pos2[0]) ** 2
    y_square = (pos1[1] - pos2[1]) ** 2
    return (x_square + y_square) ** .5


# pos2在pos1的什么方位
def get_direction(pos1, pos2):
    res = Vector2((1, 0)).angle_to(Vector2((pos2[0]-pos1[0], pos2[1]-pos1[1])))
    if res < 0:
        return res + 360
    else:
        return res

def _get_direction(pos1, pos2):
    if abs(pos1[0]-pos2[0])/setting.WORLD_SIZE < .01:
        if pos1[1] > pos2[1]:
            return 0
        else:
            return setting.PI
    if abs(pos1[1]-pos2[1])/setting.WORLD_SIZE < .01:
        if pos1[0] > pos2[0]:
            return setting.PI*1.5
        else:
            return setting.PI*.5

    if pos1[0] > pos2[0]:
        if pos1[1] > pos2[1]:
            return setting.PI-abs(math.atan(abs(pos1[0]-pos2[0])/abs(pos1[1]-pos2[1])))
        else:
            return abs(math.atan(abs(pos1[0]-pos2[0])/abs(pos1[1]-pos2[1])))
    else:
        if pos1[1] > pos2[1]:
            return setting.PI+abs(math.atan(abs(pos1[0]-pos2[0])/abs(pos1[1]-pos2[1])))
        else:
            return 2*setting.PI-abs(math.atan(abs(pos1[0]-pos2[0])/abs(pos1[1]-pos2[1])))


def get_infect_chance(dist):
    if dist > setting.INFECTION_RADIUS:
        return -1
    else:
        _factor = (dist/setting.INFECTION_RADIUS)**2
        prob=setting.INFECTION_CHANCE * _factor
        # prob = setting.INFECTION_CHANCE
        return prob


def get_gauss_rand(theta=1):
    a = gauss(0, theta)
    while True:
        if abs(a) < 1:
            break
        else:
            a = gauss(0, theta)
    return a

def get_new_direction(direct):
    new_direc = get_gauss_rand() * 90 + direct
    return new_direc


if __name__ == '__main__':
    pos1 = [50, 50]
    pos2 = [50, 100]
    print(get_direction(pos1, pos2))