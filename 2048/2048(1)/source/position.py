from settings import Settings


class Pos(object):
    def __init__(self, x, y):
        self.pos = x, y

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def up_pos(self):
        return Pos(self.x, self.y + 1)

    @property
    def down_pos(self):
        return Pos(self.x, self.y - 1)

    @property
    def left_pos(self):
        return Pos(self.x - 1, self.y)

    @property
    def right_pos(self):
        return Pos(self.x + 1, self.y)

    def pos_to_position(self):
        return self.x * Settings.GRID_SIZE + Settings.ORIGIN.x, \
               self.y * Settings.GRID_SIZE + Settings.ORIGIN.y

    def pos_to_mid_position(self):
        offset = 17
        return self.x * (Settings.GRID_SIZE + offset) + Settings.ORIGIN.x, \
               self.y * (Settings.GRID_SIZE + offset) + Settings.ORIGIN.y

    @classmethod
    def position_to_pos(cls, x, y):
        return cls((x - Settings.ORIGIN.x) // Settings.GRID_SIZE, (y - Settings.ORIGIN.y) // Settings.GRID_SIZE)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if self.pos == other.pos:
            return True
        return False

    def __add__(self, other):
        if isinstance(other, tuple):
            return Pos(self.x + other[0], self.y + other[1])
        elif isinstance(other, Pos):
            return Pos(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self + other

    def __iter__(self):
        yield self.x
        yield self.y

    @staticmethod
    def check_valid(x, y):
        if x < 0 or x >= Settings.COLUMNS or y < 0 or y >= Settings.ROWS:
            return False
        return True
