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

    def pos_to_position(self):
        return self.x * Settings.GRID_SIZE + Settings.ORIGIN.x, \
               self.y * Settings.GRID_SIZE + Settings.ORIGIN.y

    def pos_to_mid_position(self):
        return self.x * Settings.GRID_SIZE + Settings.ORIGIN.x, \
               self.y * Settings.GRID_SIZE + Settings.ORIGIN.y

    @classmethod
    def position_to_pos(cls, x, y):
        return cls((x - Settings.ORIGIN.x) // Settings.GRID_SIZE, (y - Settings.ORIGIN.y) // Settings.GRID_SIZE)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if self.pos == other.pos:
            return True
        return False

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    @staticmethod
    def check_valid(x, y):
        if x < 0 or x >= Settings.COLUMNS or y < 0 or y >= Settings.ROWS:
            return False
        return True
