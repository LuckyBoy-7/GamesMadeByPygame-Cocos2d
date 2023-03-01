from settings import Settings
from widgets import all_permutations


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
        return self.x * Settings.grid_size + Settings.origin.x, \
               self.y * Settings.grid_size + Settings.origin.y

    def pos_to_mid_position(self):
        return (self.x + 0.5) * Settings.grid_size + Settings.origin.x, \
               (self.y + 0.5) * Settings.grid_size + Settings.origin.y

    @classmethod
    def position_to_pos(cls, x, y):
        return cls((x - Settings.origin.x) // Settings.grid_size, (y - Settings.origin.y) // Settings.grid_size)

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
        if x < 0 or x >= Settings.columns or y < 0 or y >= Settings.rows:
            return False
        return True

    def search_mines(self, mines):
        mines_count = 0
        for pos in all_permutations([-1, 0, 1]):
            pos = self + pos
            if self.check_valid(*pos) and not pos == self:
                if pos in mines:
                    mines_count += 1
        return mines_count

    def get_grids_nearby(self, up_masks, flags):
        # 可以闪烁的grid
        poses = []
        for pos in all_permutations([-1, 0, 1]):
            pos = self + pos
            if self.check_valid(*pos):
                if pos not in up_masks and pos not in flags:
                    poses.append(Pos(*pos))
        return poses

    def count_flags(self, flags):
        count = 0
        for pos in all_permutations([-1, 0, 1]):
            pos = self + pos
            if pos in flags:
                count += 1
        return count

    def auto_remove(self, flags, game_layer):
        poses = []  # 要移除的格子
        for pos in all_permutations([-1, 0, 1]):
            pos = self + pos
            if self.check_valid(*pos):
                if pos not in flags and pos not in game_layer.up_masks:
                    poses.append(Pos(*pos))

        for pos in poses:
            if pos not in game_layer.nums and pos not in game_layer.mines:  # 空白
                game_layer.recursively_expand(pos)
            else:
                game_layer.set_mask(pos)

            game_layer.judge_success(pos)
