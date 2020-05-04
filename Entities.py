import random
import setting
import math


class Entity:

    def __init__(self, walk_speed=setting.WALK_SPEED):
        # 这里status应为Status类型
        self.__status = Status()
        self.__location = [0, 0]
        self.walk_speed = walk_speed
        # 在屏幕中向下是0，即与屏幕的y轴正方向同向时是0，顺时针增加
        self.walk_direction = 0
        self.id = -1

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, coordinates):
        self.__location = coordinates

    def entity_init(self, world_size, id):
        self.location = [random.uniform(0, world_size), random.uniform(0, world_size)]
        self.id = id
        self.walk_direction = random.randrange(0, 360)

    def visit_consider(self, visit_prob):
        if random.random() <= visit_prob:
            return True
        else:
            return False

    def walk(self):
        # 每帧走的距离
        if 0 <= self.walk_direction <= 90:
            x = self.location[0]-(setting.WALK_SPEED/setting.FPS)*math.sin(self.walk_direction/360)
            y = self.location[1]+(setting.WALK_SPEED/setting.FPS)*math.cos(self.walk_direction/360)
        elif 90 < self.walk_direction <= 180:
            x = self.location[0]-(setting.WALK_SPEED/setting.FPS)*math.sin((180-self.walk_direction)/360)
            y = self.location[1]-(setting.WALK_SPEED/setting.FPS)*math.cos((180-self.walk_direction)/360)
        elif 180 < self.walk_direction <= 270:
            x = self.location[0]+(setting.WALK_SPEED/setting.FPS)*math.sin((self.walk_direction-180)/360)
            y = self.location[1]-(setting.WALK_SPEED/setting.FPS)*math.cos((self.walk_direction-180)/360)
        else:
            x = self.location[0]+(setting.WALK_SPEED/setting.FPS)*math.sin((360-self.walk_direction)/360)
            y = self.location[1]+(setting.WALK_SPEED/setting.FPS)*math.cos((360-self.walk_direction)/360)
        _new_dirction = random.gauss(0, 1)*360 + self.walk_direction
        self.walk_direction = _new_dirction
        self.location = [x, y]


class Status:

    def __init__(self, is_infected=0, is_quarantined=0, is_visiting=0):
        # 0表示未感染，1及以上表示感染的天数
        self.__is_infected = is_infected
        self.__is_quarantined = is_quarantined
        self.__is_visiting = is_visiting

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