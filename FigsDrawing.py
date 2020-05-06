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

    def draw_move_seq(self, screen, pool, seq_indicator):
        for key, ent in pool.items():
            if ent.status.is_visiting > 0:
                continue
            _width = setting.RESOLUTION/setting.WORLD_SIZE
            x, y = ent.move_seq[seq_indicator]
            x = int(round(x * _width, 0))
            y = int(round(y * _width, 0))
            coordinates = (x, y)
            _radius = int(round(_width/2, 0))
            if ent.status.is_visiting > 0:
                continue
            if ent.status.is_infected > 0:
                color = (200, 0, 0)
                pygame.draw.circle(screen, color, coordinates, _radius)
                if ent.is_dist_kept:
                    color = (0, 0, 200)
                _big_radius = int(round(setting.INFECTION_RADIUS*_width, 0))
                pygame.draw.circle(screen, color, coordinates, _big_radius, 1)
            else:
                if ent.is_dist_kept:
                    color = (0, 0, 200)
                else:
                    color = (50, 50, 50)
                pygame.draw.circle(screen, color, coordinates, _radius)


def fig_draw(data):
    pyplot.figure("感染人数")
    pyplot.ion()
    pyplot.cla()
    pyplot.style.use('ggplot')
    pyplot.plot(data['time'], data['total_num_infected'], '-', label='总感染人数')
    pyplot.plot(data['time'], data['num_cur_infected'], '-', label='当前感染人数')
    pyplot.xlabel('时间')
    pyplot.ylabel('人数')
    pyplot.title('新冠疫情传播状况')
    pyplot.legend(loc='best')
    pyplot.grid()
    pyplot.pause(0.03)

def string_draw(screen, string, string2):
    font = pygame.font.SysFont('Arial', 20)
    string_render = font.render(f'R0 is: {string}, Time is: {string2}', True, (100, 100, 100))
    string_rect = string_render.get_rect()
    string_rect.topleft = (0, 0)
    screen.blit(string_render, string_rect)
