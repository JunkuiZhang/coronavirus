import SomeMath
import Virus
import random
import setting


class World:

    def __init__(self, communities, quarantine_factor=setting.QUARANTINE_FACTOR):
        self.communities = communities
        self.virus_setting = Virus.VirusSpread()
        self.new_entity_pool = self.communities.entity_pool.copy()
        self.new_infected_pool = self.communities.infected_pool.copy()
        self.world_time = 0
        self.quarantine_factor = quarantine_factor
        self.data = {'time': [], 'num': [], 'num_cur_infected': []}

    def live_one_day(self, a_day_indicator):
        self.new_infected_pool = self.communities.infected_pool.copy()
        self.new_entity_pool = self.communities.entity_pool.copy()
        if a_day_indicator:
            self.data['time'].append(self.world_time)
            self.data['num'].append(setting.POP_SIZE-len(self.communities.entity_pool))
            self.data['num_cur_infected'].append(setting.POP_SIZE-len(self.communities.entity_pool)
                                                 -len(self.communities.quarantined_pool))
        for inf_key, inf_ent in self.communities.infected_pool.items():
            inf_pos = inf_ent.location
            for nor_key, nor_ent in self.communities.entity_pool.items():
                dist = SomeMath.dist_cal(nor_ent.location, inf_pos)
                if dist <= self.virus_setting.infection_radius:
                    if self.new_entity_pool.get(nor_key) is None:
                        continue
                    if random.random() <= SomeMath.get_infect_chance(dist):
                        self.new_infected_pool[nor_key] = self.new_entity_pool.pop(nor_key)
        for key, ent in self.new_infected_pool.items():
            ent.status.is_infected += 1
        self.communities.entity_pool = self.new_entity_pool.copy()
        self.communities.infected_pool = self.new_infected_pool.copy()
        self.communities.community_central_park()
        self.communities.quarantine()
        self.communities.community_move(a_day_indicator)
        if a_day_indicator:
            self.world_time += 1
