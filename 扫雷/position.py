from grid_objs import Mine
from settings import Settings


class Pos(object):
    def __init__(self, pos):
        self.pos = pos

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def up_pos(self):
        return Pos((self.pos[0], self.pos[1] + 1))

    @property
    def down_pos(self):
        return Pos((self.pos[0], self.pos[1] - 1))

    @property
    def left_pos(self):
        return Pos((self.pos[0] - 1, self.pos[1]))

    @property
    def right_pos(self):
        return Pos((self.pos[0] + 1, self.pos[1]))

    def pos_to_position(self):
        return self.pos[0] * Settings.GRID_SIZE + Settings.ORIGIN[0], \
               self.pos[1] * Settings.GRID_SIZE + Settings.ORIGIN[1]

    def pos_to_mid_position(self):
        return (self.pos[0] + 0.5) * Settings.GRID_SIZE + Settings.ORIGIN[0], \
               (self.pos[1] + 0.5) * Settings.GRID_SIZE + Settings.ORIGIN[1]

    @classmethod
    def position_to_pos(cls, x, y):
        return cls(((x - Settings.ORIGIN[0]) // Settings.GRID_SIZE, (y - Settings.ORIGIN[1]) // Settings.GRID_SIZE))

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if isinstance(other, tuple):
            if self.pos == other:
                return True
        if isinstance(other, Pos):
            if self.pos == other.pos:
                return True
        return False

    @staticmethod
    def check_valid(x, y):
        if x < 0 or x >= Settings.ROWS or y < 0 or y >= Settings.COLUMNS:
            return False
        return True

    def search_around(self, layer, judge):
        matches = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pos = self.x + i, self.y + j
                if self.check_valid(*pos):
                    if bool(layer[pos]) == bool(judge):
                        matches.append(pos)
        return matches

    def search_mines(self, grids):
        mines_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pos = self.x + i, self.y + j
                if self.check_valid(*pos) and not pos == self.pos:
                    if grids[pos] is Mine:
                        mines_count += 1
        return mines_count

    def get_mask_nearby(self, up_masks):
        poses = self.search_around(up_masks, not None)
        return poses

    def count_flags(self, flags):
        flag_count = len(self.search_around(flags, not None))
        return flag_count

    def auto_remove(self, flags, game_layer):
        poses = self.search_around(flags, None)
        for pos in poses:
            if game_layer.grids[pos] is None:
                game_layer.recursively_expand(Pos(pos))
            else:
                game_layer.remove_mask(pos)

            if game_layer.grids[pos] is Mine:
                game_layer.show_all_mines()
