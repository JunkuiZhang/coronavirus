import Virus
import setting


class World:

    def __init__(self, communities, quarantine_factor=setting.QUARANTINE_FACTOR):
        self.communities = communities
        self.virus_setting = Virus.VirusSpread()
        self.world_time = 0
        self.quarantine_factor = quarantine_factor
        self.data = {'total_num_quarantined': 0, 'total_num_infected': [len(communities.infected_id_pool)],
                     'num_cur_infected': [len(communities.infected_id_pool)], 'r0': None, 'time':[0]}
        self.one_frame_data = {'get_infected_by':[], 'delta_infected':0, 'is_quarantined':0, 'park_infected':0}
        self.park_indicator = [0, 0, 0]
        self.frames_data = {'num_get_infected_by':0, 'delta_infected':0, 'is_quarantined':0, 'park_infected':0}
        self.infected_id_pool = communities.infected_id_pool

    def live_one_day(self, a_day_indicator, group, screen, big_pos_list, dist_factor):
        if dist_factor:
            setting.VISIT_CHANCE = .02
        self.communities.get_neighbor()
        group.update(screen, a_day_indicator, self.one_frame_data, self.park_indicator, big_pos_list, dist_factor,
                     self.data['total_num_infected'][-1])
        self.one_frame_data_proc()
        if a_day_indicator:
            self.frames_data_proc()

    def frames_data_proc(self):
        self.world_time += 1
        self.data['time'].append(self.world_time)
        _frames_data = self.frames_data
        self.park_indicator = self.park_indicator[1:]
        self.park_indicator.append(_frames_data['park_infected'])
        if _frames_data['num_get_infected_by'] == 0:
            pass
        else:
            self.data['r0'] = _frames_data['delta_infected']/_frames_data['num_get_infected_by']*setting.QUARANTINE_INTERVAL
        _indicator = self.data['total_num_infected'][-1]
        self.data['total_num_infected'].append(_frames_data['delta_infected'] + _indicator)
        self.data['total_num_quarantined'] += _frames_data['is_quarantined']
        self.data['num_cur_infected'].append(self.data['total_num_infected'][-1] - self.data['total_num_quarantined'])
        self.frames_data_reset()

    def one_frame_data_proc(self):
        _one_frame_data = self.one_frame_data
        self.frames_data['num_get_infected_by'] += len(_one_frame_data['get_infected_by'])
        self.frames_data['delta_infected'] += _one_frame_data['delta_infected']
        self.frames_data['is_quarantined'] += _one_frame_data['is_quarantined']
        self.frames_data['park_infected'] = _one_frame_data['park_infected']
        self.one_frame_data_reset()

    def is_virus_gone(self):
        if  (self.data['total_num_quarantined'] == self.data['total_num_infected'][-1]) and \
                (sum(self.park_indicator) == 0):
            return True
        else:
            return False

    def one_frame_data_reset(self):
        self.one_frame_data = {'get_infected_by':[], 'delta_infected':0, 'is_quarantined':0, 'park_infected':0}

    def frames_data_reset(self):
        self.frames_data = {'num_get_infected_by':0, 'delta_infected': 0, 'is_quarantined': 0, 'park_infected': 0}
