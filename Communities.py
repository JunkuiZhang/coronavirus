import Entities
import random
import setting
import SomeMath
import pygame
from pygame.math import Vector2


class Community:

    def __init__(self, size, world_size):
        self.__size = size
        self.__world_size = world_size
        self.__entity_pool = {}
        self.__infected_id_pool = []
        self.quarantined_pool = {}
        self.central_park_id_pool = []
        self.central_park_considered = []
        self.central_park_indicator = [0, 0, 0]
        # 度量r0时，防止重复计算
        self.infected_considered_id_pool = []
        self.r0_pool = []
        self.r0 = 0

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def world_size(self):
        return self.__world_size

    @world_size.setter
    def world_size(self, value):
        self.__world_size = value

    @property
    def entity_pool(self):
        return self.__entity_pool

    @entity_pool.setter
    def entity_pool(self, value):
        self.__entity_pool = value

    @property
    def infected_id_pool(self):
        return self.__infected_id_pool

    @infected_id_pool.setter
    def infected_id_pool(self, value):
        self.__infected_id_pool = value

    @size.setter
    def size(self, value):
        if not isinstance(value, int):
            raise ValueError('社区大小应为整数！')
        if value <= 0 or value > 1000:
            raise ValueError('社区大小应在0到1000之间')
        self.__size = value

    def clean_quaran_pool(self):
        self.quarantined_pool = {}

    def keep_dist_generator(self):
        if setting.KEEP_DIST == 0:
            return False
        else:
            if random.random() <= setting.KEEP_DIST:
                return True
            else:
                return False

    def community_init(self, group):
        infected_id = random.sample(range(self.size), int(round(self.size*setting.INITIAL_CHANCE, 0)))
        self.get_empty_big_pos()
        # infected_id = random.sample(range(self.size), 1)
        for num in range(self.size):
            ent = Entities.Entity()
            _id = num + 1
            ent.entity_init(setting.RESOLUTION, _id)
            # ent.entity_init(world_size=self.world_size, id=_id)
            ent.is_dist_kept = self.keep_dist_generator()
            self.entity_pool[f'{ent.id}'] = ent
            if _id in infected_id:
                ent.status.is_infected = 1
                self.infected_id_pool.append((f'{_id}'))
            self.big_pos_getter(ent)
            group.add(ent)

    def _get_neighbor(self):
        for key1, ent1 in self.entity_pool.items():
            for key2, ent2 in self.entity_pool.items():
                if int(key1) >= int(key2): continue
                if pygame.sprite.collide_circle(ent1, ent2):
                    ent1.neighbor_pool.append([ent2.id, ent2.location, ent2.status.is_infected])
                    ent2.neighbor_pool.append([ent1.id, ent1.location, ent1.status.is_infected])

    def get_neighbor(self):
        for key, ent in self.entity_pool.items():
            a, b = ent.big_position
            c = len(self.big_pos_list[0])
            _big_pos_l = []
            for x in range(int(a-1), int(a+2)):
                if x < 0 or x >= c:
                    continue
                for y in range(int(b-1), int(b+2)):
                    if y < 0 or y >= c:
                        continue
                    if len(self.big_pos_list[x][y]) == 0:
                        continue
                    for neighbor in self.big_pos_list[x][y]:
                        if neighbor[0] == int(ent.id):
                            continue
                        if Vector2(ent.location).distance_to(Vector2(neighbor[1])) <= 1.5*setting.INFECTION_RADIUS:
                        # if ent.location.distant_to(neighbor[1]) <= setting.INFECTION_RADIUS:
                            ent.neighbor_pool.append(neighbor)

    def __get_neighbor(self):
        for key1 in self.entity_pool:
            for key2 in self.entity_pool:
                if key1 >= key2:
                    continue
                pos1 = self.entity_pool[f'{key1}'].location
                pos2 = self.entity_pool[f'{key2}'].location
                if SomeMath.dist_cal(pos1, pos2) <= setting.INFECTION_RADIUS:
                    _is_here_1 = self.entity_pool[f'{key1}'].status.is_visiting == 0
                    _is_infected_1 = self.entity_pool[f'{key1}'].status.is_infected
                    _is_here_2 = self.entity_pool[f'{key2}'].status.is_visiting == 0
                    _is_infected_2 = self.entity_pool[f'{key2}'].status.is_infected
                    self.entity_pool[f'{key1}'].neighbor_pool.append([key2, pos2, _is_here_2, _is_infected_2])
                    self.entity_pool[f'{key2}'].neighbor_pool.append([key1, pos1, _is_here_1, _is_infected_1])

    def get_infected_visitor(self):
        res = 0
        for key in self.central_park_id_pool:
            if self.entity_pool[key].status.is_infected > 0:
                res += 1
        return res

    def get_empty_big_pos(self):
        m, n = setting.BIN_X, setting.BIN_Y
        self.big_pos_list = [[[] for i in range(m)] for j in range(n)]

    def big_pos_getter(self, ent):
        _x = int(ent.big_position[0])
        _y = int(ent.big_position[1])
        if ent.status.is_quarantined + ent.status.is_visiting > 0:
            _is_here = False
        else:
            _is_here = True
        self.big_pos_list[_x][_y].append([ent.id, ent.location, ent.status.is_infected, _is_here])

    def community_go_one_frame(self, one_day_indicator):
        res = {
                'infect': [], 'is_quarantined': [], 'is_visiting': [], 'visit_leave': []
              }
        self.big_pos_list = self.big_pos_list_init()
        num_infected = len(self.infected_id_pool)
        self.infected_considered_id_pool = []
        for key, ent in self.entity_pool.items():
            if key in self.infected_id_pool:
                res1 = ent.live_one_frame_infected(one_day_indicator)
                self.res_infected_check(res1, res, key)
            elif key in self.central_park_id_pool:
                num1 = self.get_infected_visitor()
                if num1 > 0:
                    assert len(self.central_park_indicator) == 2
                    self.central_park_indicator.append(1)
                else:
                    assert len(self.central_park_indicator) == 2
                    self.central_park_indicator.append(0)
                res2 = ent.live_one_day_visiting(one_day_indicator, self.central_park_indicator)
                num2 = self.get_infected_visitor()
                self.central_park_r0 = self.res_visiting_check(res2, key, num1, num2, res)
            else:
                res3 = ent.live_one_frame_susceptible(one_day_indicator)
                self.res_susceptible_check(res3, key, res)
            self.big_pos_getter(ent)

        if len(res['infect']) > 0:
            for _id in res['infect']:
                if _id not in self.infected_considered_id_pool:
                    self.infected_considered_id_pool.append(_id)
                    self.infected_id_pool.append(_id)
                    self.entity_pool[f'{_id}'].status.is_infected = 1
        if num_infected > 0:
            self.r0_pool.append(len(self.infected_considered_id_pool)/num_infected)
        else:
            self.r0_pool.append(1)
        if len(res['is_quarantined']) > 0:
            for _id in res['is_quarantined']:
                self.infected_id_pool.remove(f'{_id}')
                self.quarantined_pool[f'{_id}'] = self.entity_pool.pop(f'{_id}')
        if len(res['is_visiting']) > 0:
            for _id in res['is_visiting']:
                self.central_park_id_pool.append(_id)
                self.entity_pool[_id].status.is_visiting += 1
                if self.entity_pool[f'{_id}'].status.is_infected > 0:
                    self.infected_id_pool.remove(_id)
        if one_day_indicator:
            self.r0 = sum(self.r0_pool)
        if len(res['visit_leave']) > 0:
            for _id in res['visit_leave']:
                self.central_park_id_pool.remove(_id)
                self.entity_pool[_id].status.is_visiting = 0
                if self.entity_pool[_id].status.is_infected > 0:
                    self.infected_id_pool.append(_id)

    def res_infected_check(self, res1, data, id):
        if len(res1['infect']) > 0:
            for key in res1['infect']:
                data['infect'].append(key)
        if res1['is_quarantined'] > 0:
            data['is_quarantined'].append(id)
        if res1['is_visiting'] > 0:
            data['is_visiting'].append(id)
        return data

    def res_visiting_check(self, res, id, num1, num2, data):
        if res[0] == 0:
            data['visit_leave'].append(id)
        self.central_park_indicator = self.central_park_indicator[1:]
        return (num2-num1)/num1

    def res_susceptible_check(self, res, id, data):
        if res['visit_consider'] > 0:
            data['is_visiting'].append(id)
