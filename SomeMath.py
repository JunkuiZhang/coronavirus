import setting


def dist_cal(pos1, pos2):
    x_square = (pos1[0] - pos2[0]) ** 2
    y_square = (pos1[1] - pos2[1]) ** 2
    return (x_square + y_square) ** .5


def get_infect_chance(dist):
    prob=setting.INFECTION_CHANCE*((setting.INFECTION_RADIUS-dist)/setting.INFECTION_RADIUS)**2
    assert prob <= 1
    return prob
