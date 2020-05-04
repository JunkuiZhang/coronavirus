import Communities
import World
import FigsDrawing
import pygame
from pygame.locals import *
import setting
import random


if __name__ == '__main__':
    random.seed(setting.SEED)
    a = FigsDrawing.Animation()
    c = Communities.Community(size=setting.POP_SIZE, world_size=setting.WORLD_SIZE)
    c.community_init()
    c.virus_spread_begin()
    w = World.World(c)
    pygame.init()
    screen = pygame.display.set_mode((setting.RESOLUTION, setting.RESOLUTION))
    a.draw_background(screen)
    clock = pygame.time.Clock()
    clock.tick(setting.FPS)
    pygame.display.set_caption('新冠肺炎模拟')
    a.draw_pop(screen, c)
    FigsDrawing.string_draw(screen, 'None')
    # pygame.draw.line(screen, (100, 100, 100), (100, 0), (500, 500), 5)
    pygame.display.update()

    is_paused = True
    fps_indicator = 0
    time_indicator = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    is_paused = not is_paused

        if not is_paused:
            time_indicator = fps_indicator // setting.FPS
            w.live_one_day(fps_indicator%setting.FPS==0)
            a.draw_background(screen)
            a.draw_pop(screen, c)
            if w.data['r0'] is None:
                _r0 = 'None'
            else:
                _r0 = round(w.data['r0']*5, 2)
            FigsDrawing.string_draw(screen, _r0)
            clock.tick(setting.FPS)
            pygame.display.update()
            if time_indicator % 5 == 0:
                FigsDrawing.fig_draw(w.data)
            if w.game_over_check(time_indicator%10==0):
                is_paused = not is_paused
            fps_indicator += 1
