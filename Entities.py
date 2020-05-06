import random
import setting
import SomeMath
from numpy import mean
import pygame
from pygame.math import Vector2


class Entity(pygame.sprite.Sprite):

    def __init__(self, location=(0, 0), walk_direction=0, is_dist_kept=False):
        pygame.sprite.Sprite.__init__(self)
        # 这里status应为Status类型
        self.location =Vector2(location)
        self.image = pygame.Surface((setting.INFECTION_RADIUS, setting.INFECTION_RADIUS), pygame.SRCALPHA)
        self.__status = Status()
        # 在屏幕右向是0，即与屏幕的x轴正方向同向时是0，顺时针增加
        self.walk_direction = walk_direction
        self.velocity = Vector2((1, 0)).rotate(self.walk_direction) * setting.WALK_SPEED
        self.rect = self.image.get_rect(center=self.location)
        self.is_dist_kept = is_dist_kept
        # 检测半径
        self.radius = setting.INFECTION_RADIUS
        self.id = -1
        self.neighbor_pool = []
        self.neighbor_direction_pool = []
        self.big_position = []
        self.need_get_back = False
        self.move_seq = []

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def big_pos_get(self):
        _x, _y = self.location
        _a = _x // setting.BIN_X
        _b = _y // setting.BIN_Y
        self.big_position = [int(_a), int(_b)]

    def entity_init(self, world_size, id):
        _x = random.randint(0, world_size)
        _y = random.randint(0, world_size)
        self.location = [_x, _y]
        self.big_pos_get()
        self.id = id
        self.walk_direction = random.randrange(0, 360)

    def update(self, screen, one_day_indicator, data, park_indicator, big_pos_list):
        if self.status.is_visiting + self.status.is_quarantined > 0:
            _is_here = False
        else:
            _is_here = True
        _info = [self.id, self.location, self.status.is_infected, _is_here]
        if self.status.is_quarantined == 1: self.kill()
        if self.status.is_visiting == 0:
            if self.status.is_infected == 0:
                res = self.live_one_frame_susceptible(one_day_indicator)
                if res['get_infected_by']:
                    _res = []
                    for key in res['get_infected_by']:
                        if key in data['get_infected_by']:
                            continue
                        elif key not in _res:
                            _res.append(key)
                    if _res:
                        data['get_infected_by'].append(_res[0])
                    data['delta_infected'] += 1
                # if res['is_visiting']:
                #     data['is_visiting'].append(self.id)
            else:
                assert self.status.is_quarantined == 0
                res = self.live_one_frame_infected(one_day_indicator)
                if res['is_quarantined'] > 0:
                    data['is_quarantined'] += 1
                    self.kill()
                if res['is_visiting'] > 0:
                    # data['is_visiting'].append(self.id)
                    assert self.status.is_quarantined == 0
                    data['park_infected'] = 1
        else:
            res = self.live_one_day_visiting(one_day_indicator, park_indicator)
            if res[1] > 0:
                data['delta_infected'] += 1
        _x = int(self.big_position[0])
        _y = int(self.big_position[1])
        self.big_pos_get()
        self.big_pos_list_update(big_pos_list, (_x, _y), _info)
        self.big_pos_get()
        if self.status.is_quarantined == 0: self.draw_self(screen)

    def num_of_infected_reset(self):
        self.status.num_of_infected = 0

    def big_pos_list_update(self, big_pos_list, _big_pos, _info):
        _id = self.id
        _loc = self.location
        _inf = self.status.is_infected
        x = int(self.big_position[0])
        y = int(self.big_position[1])
        _x = int(_big_pos[0])
        _y = int(_big_pos[1])
        if self.status.is_visiting + self.status.is_quarantined > 0:
            _is_here = False
        else:
            _is_here = True
        if self.status.is_quarantined == 0:
            big_pos_list[_x][_y].remove(_info)
            big_pos_list[x][y].append([_id, _loc, _inf, _is_here])
        else:
            big_pos_list[_x][_y].remove(_info)

    def infection_check(self, dist):
        # if random.random() <= SomeMath.get_infect_chance(dist):
        if random.random() <= SomeMath.get_infect_chance(dist):
            return True
        else:
            return False

    def draw_self(self, screen):
        entity_radius = int(setting.INFECTION_RADIUS*.2)
        pos = (int(self.location[0]), int(self.location[1]))
        if self.status.is_infected > 0:
            if self.status.is_visiting > 0:
                color = (0, 200, 0)
            else:
                color = (200, 0, 0)
            pygame.draw.circle(screen, color, pos, entity_radius)
            if self.is_dist_kept:
                color = (0, 0, 200)
            pygame.draw.circle(screen, color, pos, self.radius, 1)
        else:
            if self.is_dist_kept:
                color = (0, 0, 200)
            elif self.status.is_visiting > 0:
                color = (0, 200, 0)
            else:
                color = (50, 50, 50)
            pygame.draw.circle(screen, color, pos, entity_radius)

    def visiting_consider(self):
        assert self.status.is_visiting == 0
        if random.random() <= setting.VISIT_CHANCE:
            self.status.is_visiting = 1

    def infection_during_visiting(self, park_indicator):
        if random.random() <= setting.visit_infected_chance(park_indicator):
            return 1
        else:
            return 0

    def position_bound_check(self):
        if self.location[0] < 0:
            self.location[0] += setting.RESOLUTION
        if self.location[0] > setting.RESOLUTION:
            self.location[0] = self.location[0]-setting.RESOLUTION
        if self.location[1] < 0:
            self.location[1] += setting.RESOLUTION
        if self.location[1] > setting.RESOLUTION:
            self.location[1] = self.location[1] - setting.RESOLUTION

    def live_one_frame(self, one_day_indicator, infect_indicator):
        assert self.neighbor_direction_pool == []
        _infect_list = []
        for n in range(len(self.neighbor_pool)):
            key = self.neighbor_pool[n][0]
            pos = self.neighbor_pool[n][1]
            is_infected = self.neighbor_pool[n][2]
            is_here = self.neighbor_pool[n][3]
            if not is_here: continue
            self.neighbor_direction_pool.append(SomeMath.get_direction(self.location, pos))
            if infect_indicator == 0 and is_infected > 0:
                # dis = SomeMath.dist_cal(self.location, pos)
                pos1 = Vector2(self.location)
                pos2 = Vector2(pos)
                dis = pos1.distance_to(pos2)
                if self.infection_check(dis):
                    self.status.is_infected = 1
                    _infect_list.append(key)
        if len(self.neighbor_direction_pool) > 0 and self.is_dist_kept:
            self.walk_direction = mean(self.neighbor_direction_pool)-180
        else:
            pass
        self.neighbor_direction_pool = []
        self.neighbor_pool = []
        self.walk()
        if infect_indicator > 0:
            return {'get_infected_by': _infect_list}
        else:
            return {'get_infected_by': _infect_list}

    def live_one_frame_susceptible(self, one_day_indicator):
        assert self.status.is_visiting == 0
        _is_visiting = 0
        res = self.live_one_frame(one_day_indicator, self.status.is_infected)
        if one_day_indicator:
            self.visiting_consider()
        if self.status.is_visiting > 0:
            res['is_visiting'] = self.id
            return res
        else:
            res['is_visiting'] = None
            return res

    def live_one_frame_infected(self, one_day_indicator):
        assert self.status.is_infected > 0
        res = self.live_one_frame(one_day_indicator, self.status.is_infected)
        if one_day_indicator:
            if self.status.is_infected > setting.QUARANTINE_INTERVAL:
                if random.random() <= setting.QUARANTINE_CHANCE:
                    self.status.is_quarantined = 1
            else:
                self.visiting_consider()
            self.status.is_infected += 1
        res['is_quarantined'] = self.status.is_quarantined
        res['is_visiting'] = self.status.is_visiting
        return res

    def live_one_day_visiting(self, one_day_indicator, park_indi):
        _get_infected = 0
        if one_day_indicator:
            self.status.is_visiting += 1
            if self.status.is_visiting > setting.VISIT_DURATION + 1:
                self.status.is_visiting = 0
            if self.status.is_infected == 0:
                self.status.is_infected = self.infection_during_visiting(park_indi)
                if self.status.is_infected > 0: _get_infected = 1
        return self.status.is_visiting, _get_infected

    def check_dist(self, pos):
        if SomeMath.dist_cal(self.location, pos) < setting.INFECTION_RADIUS and self.is_dist_kept:
            _new_direct = SomeMath.get_direction(self.location, pos)
            self.walk_direction = abs(_new_direct - setting.PI)
        else:
            pass

    def get_new_direction(self):
        self.walk_direction = SomeMath.get_new_direction(self.walk_direction)

    def walk(self):
        # 每帧走的距离
        self.velocity = Vector2((1,0)).rotate(self.walk_direction)*setting.WALK_SPEED
        self.location += self.velocity
        self.position_bound_check()
        self.rect.center = self.location
        self.get_new_direction()
        # self.walk_direction = random.randint(0, 360)


class Status:

    def __init__(self, is_infected=0, is_quarantined=0, is_visiting=0, num_of_infected=0):
        # 0表示未感染，1及以上表示感染的天数
        self.__is_infected = is_infected
        self.__is_quarantined = is_quarantined
        self.__is_visiting = is_visiting
        self.__num_of_infected = num_of_infected

    def status_value_check(self, value):
        if not isinstance(value, int):
            raise ValueError('状态变量不是整数')
        else:
            return value

    @property
    def is_infected(self):
        return self.__is_infected

    @is_infected.setter
    def is_infected(self, value):
        self.__is_infected = value

    @property
    def is_quarantined(self):
        return self.__is_quarantined

    @is_quarantined.setter
    def is_quarantined(self, value):
        self.__is_quarantined = self.status_value_check(value)

    @property
    def is_visiting(self):
        return self.__is_visiting

    @is_visiting.setter
    def is_visiting(self, value):
        self.__is_visiting = self.status_value_check(value)

    @property
    def num_of_infected(self):
        return self.__num_of_infected

    @num_of_infected.setter
    def num_of_infected(self, value):
        self.__num_of_infected = value
