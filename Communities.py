class Community:

    def __init__(self, size):
        self.__size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        if not isinstance(value, int):
            raise ValueError('社区大小应为整数！')
        if value <= 0 or value > 1000:
            raise ValueError('社区大小应在0到1000之间')
        self.__size = value

