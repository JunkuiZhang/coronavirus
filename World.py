import Entities


class World:

    def __init__(self, pop_num, world_size=1000):
        self.__pop_num = pop_num
        self.__world_size = world_size

    @property
    def pop_num(self):
        return self.__pop_num

    @property
    def world_size(self):
        return self.__world_size

    def generate(self):
        pass