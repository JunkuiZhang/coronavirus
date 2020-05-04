from matplotlib import pyplot
import pygame
import setting


pyplot.rcParams['font.sans-serif'] = ['SimHei']
pyplot.rcParams['axes.unicode_minus'] = False


class Animation:

    def __init__(self):
        pass

    def draw_background(self, screen, color=setting.BACKGROUND_COLOR):
        screen.fill(color)

    def draw_pool(self, screen, pool, is_infected):
        for key, ent in pool.items():
            _width = setting.RESOLUTION/setting.WORLD_SIZE
            x, y = ent.location
            x = int(round(x * _width, 0))
            y = int(round(y * _width, 0))
            # x = x * _width
            # y = y * _width
            coordinates = (x, y)
            _radius = int(round(_width/2, 0))
            if is_infected:
                color = (200, 0, 0)
                pygame.draw.circle(screen, color, coordinates, _radius)
                _big_radius = int(round(setting.INFECTION_RADIUS*_width, 0))
                pygame.draw.circle(screen, color, coordinates, _big_radius, 1)
            else:
                color = (50, 50, 50)
                pygame.draw.circle(screen, color, coordinates, _radius)

    def draw_pop(self, screen, communities):
        self.draw_pool(screen, communities.entity_pool, False)
        self.draw_pool(screen, communities.infected_pool, True)


def fig_draw(data):
    pyplot.figure("感染人数")
    pyplot.ion()
    pyplot.cla()
    pyplot.style.use('ggplot')
    pyplot.plot(data['time'], data['num'], '-', label='总感染人数')
    pyplot.plot(data['time'], data['num_cur_infected'], '-', label='当前感染人数')
    pyplot.xlabel('时间')
    pyplot.ylabel('人数')
    pyplot.title('新冠疫情传播状况')
    pyplot.legend(loc='best')
    pyplot.grid()
    pyplot.pause(0.03)