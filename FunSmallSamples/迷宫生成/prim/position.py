from settings import Settings


class Pos(object):
    def __init__(self, x: int, y: int):
        self.pos = x, y

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def pos_to_position(self):  # 从pos知道该画在哪里
        return self.x * Settings.GRID_SIZE + Settings.ORIGIN[0], \
               self.y * Settings.GRID_SIZE + Settings.ORIGIN[1]

    @classmethod
    def position_to_pos(cls, x, y):  # 从position和ORIGIN推出对应网格坐标
        return cls((x - Settings.ORIGIN[0]) // Settings.GRID_SIZE, (y - Settings.ORIGIN[1]) // Settings.GRID_SIZE)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if self.pos == other.pos:
            return True
        return False

    def __iter__(self):
        yield self.x
        yield self.y
