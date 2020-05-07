import Communities
import World
import FigsDrawing
import pygame
from pygame.locals import *
import setting
import random


if __name__ == '__main__':
    if setting.SEED:
        random.seed(setting.SEED)
    a = FigsDrawing.Animation()
    c = Communities.Community(size=setting.POP_SIZE, world_size=setting.WORLD_SIZE)
    group = pygame.sprite.Group()
    c.community_init(group)
    w = World.World(c)
    pygame.init()
    screen = pygame.display.set_mode((setting.RESOLUTION, setting.RESOLUTION))
    a.draw_background(screen)
    clock = pygame.time.Clock()
    clock.tick(setting.FPS)
    pygame.display.set_caption('疫情模拟 | 张峻魁')
    # a.draw_pop(screen, c)
    # group.update(screen, False, )
    FigsDrawing.string_draw(screen, 'None', 0)
    # pygame.draw.line(screen, (100, 100, 100), (100, 0), (500, 500), 5)
    pygame.display.update()

    is_paused = True
    fps_indicator = 1
    time_indicator = 0
    dist_keep_change = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    is_paused = not is_paused
                if event.key == K_RETURN:
                    dist_keep_change = not dist_keep_change

        if not is_paused:
            clock.tick(setting.FPS)
            time_indicator = fps_indicator // setting.FPS
            is_one_day_finished = fps_indicator%setting.FPS == 0
            a.draw_background(screen)
            w.live_one_day(is_one_day_finished, group, screen, c.big_pos_list, dist_keep_change)
            if w.data['r0'] is None:
                _r0 = 'None'
            else:
                _r0 = round(w.data['r0'], 2)
            FigsDrawing.string_draw(screen, _r0, time_indicator)
            pygame.display.update()
            if w.is_virus_gone():
                is_paused = not is_paused
            if time_indicator % 5 == 0:
                FigsDrawing.fig_draw(w.data, dist_keep_change)
            fps_indicator += 1
