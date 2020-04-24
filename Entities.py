import random


class Entity:

    def __init__(self, status, location, community, walk_speed=10):
        # 这里status应为Status类型
        self.status = status
        self.__location = location
        self.walk_speed = walk_speed
        self.community = community

    def walk(self):
        coordinates = [0, 0]
        coordinates[0] = random.randint(1, self.community.size)
        coordinates[1] = random.randint(1, self.community.size)
        self.location = coordinates

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, coordinates):
        self.__location = coordinates


class Status:

    def __init__(self, is_infected, is_isolated, is_visiting=0):
        self.__is_infected = is_infected
        self.__is_isolated = is_isolated
        self.__is_visiting = is_visiting

    def status_value_check(self, value):
        if not isinstance(value, int):
            raise ValueError('状态变量不是整数')
        if value == 0 or value == 1:
            return value
        else:
            raise ValueError('状态变量只能是0或1')

    @property
    def is_infected(self):
        return self.__is_infected

    @is_infected.setter
    def is_infected(self, value):
        self.__is_infected = self.status_value_check(value)

    @property
    def is_isolated(self):
        return self.__is_isolated

    @is_isolated.setter
    def is_isolated(self, value):
        self.__is_isolated = self.status_value_check(value)

    @property
    def is_visiting(self):
        return self.__is_visiting

    @is_visiting.setter
    def is_visiting(self, value):
        self.__is_visiting = self.status_value_check(value)