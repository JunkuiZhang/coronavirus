import Entities
import random
import setting


class Community:

    def __init__(self, size, world_size):
        self.__size = size
        self.__world_size = world_size
        self.__entity_pool = {}
        self.__infected_pool = {}
        self.quarantined_pool = {}
        self.central_park_pool = {}
        self.central_park_indicator = [0, 0, 0]

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
    def infected_pool(self):
        return self.__infected_pool

    @infected_pool.setter
    def infected_pool(self, value):
        self.__infected_pool = value

    @size.setter
    def size(self, value):
        if not isinstance(value, int):
            raise ValueError('社区大小应为整数！')
        if value <= 0 or value > 1000:
            raise ValueError('社区大小应在0到1000之间')
        self.__size = value

    def clean_quaran_pool(self):
        self.quarantined_pool = {}

    def community_init(self):
        for num in range(self.size):
            ent = Entities.Entity()
            ent.entity_init(world_size=self.world_size, id=num+1)
            self.entity_pool[f'{ent.id}'] = ent

    def virus_spread_begin(self, initial_chance=.01):
        infected_id = random.sample(range(self.size), int(round(self.size*initial_chance, 0)))
        for initial_id in infected_id:
            _id = initial_id + 1
            self.entity_pool[f'{_id}'].status.is_infected = 1
            self.infected_pool[f'{_id}'] = self.entity_pool.pop(f'{_id}')

    def community_central_park(self, visit_duration=setting.VISIT_DURATION):
        _inf_pool = self.infected_pool.copy()
        _vis_pool = self.central_park_pool.copy()
        _ent_pool = self.entity_pool.copy()
        prob = setting.visit_infected_chance(self.central_park_indicator)
        self.central_park_indicator = self.central_park_indicator[1:]
        self.central_park_indicator.append(0)
        for key in self.central_park_pool:
            assert not _vis_pool.get(key) is None
            _vis_pool[key].status.is_visiting += 1
            if _vis_pool[key].status.is_infected == 0:
                if random.random() <= prob:
                    _vis_pool[key].status.is_infected = 1
            if _vis_pool[key].status.is_visiting == visit_duration + 1:
                _vis_pool[key].status.is_visiting = 0
                if _vis_pool[key].status.is_infected == 0:
                    _ent_pool[key] = _vis_pool.pop(key)
                else:
                    _inf_pool[key] = _vis_pool.pop(key)
        self.entity_pool = _ent_pool
        self.infected_pool = _inf_pool
        self.central_park_pool = _vis_pool

    def community_move(self, visit_indicator, visit_chance=setting.VISIT_CHANCE):
        _ent_pool = self.entity_pool.copy()
        _inf_pool = self.infected_pool.copy()
        _vis_pool = self.central_park_pool.copy()
        for key in self.entity_pool:
            if _ent_pool[key].visit_consider(visit_chance) and visit_indicator:
                _ent_pool[key].status.is_visiting = 1
                _vis_pool[key] = _ent_pool.pop(key)
            else:
                _ent_pool[key].walk()
        for key in self.infected_pool:
            if _inf_pool[key].visit_consider(visit_chance) and visit_indicator:
                _inf_pool[key].status.is_visiting = 1
                self.central_park_indicator[2] = 1
                _vis_pool[key] = _inf_pool.pop(key)
            else:
                _inf_pool[key].walk()
        self.entity_pool = _ent_pool
        self.infected_pool = _inf_pool
        self.central_park_pool = _vis_pool

    def quarantine(self, chance=setting.QUARANTINE_CHANCE, interval=setting.QUARANTINE_INTERVAL):
        new_infect_pool = self.infected_pool.copy()
        new_quaran_pool = self.quarantined_pool.copy()
        for key, ent in self.infected_pool.items():
            if ent.status.is_infected >= interval+1:
                if random.random() <= chance:
                    new_infect_pool[key].is_quarantined = 1
                    new_quaran_pool[key] = new_infect_pool.pop(key)
        self.infected_pool = new_infect_pool.copy()
        self.quarantined_pool = new_quaran_pool.copy()
