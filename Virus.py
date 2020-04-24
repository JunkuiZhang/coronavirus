class VirusSpread:

    def __init__(self, infection_radius=10, infection_chance=.2):
        self.infection_radius = infection_radius
        self.__infection_chance = infection_chance

    @property
    def infection_chance(self):
        return self.__infection_chance

    @infection_chance.setter
    def infection_chance(self, value):
        if not (0 < value and value < 1):
            raise ValueError('感染概率应处在0和1之间')