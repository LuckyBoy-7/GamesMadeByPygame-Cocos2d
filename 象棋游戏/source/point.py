class Point(object):
    def __init__(self, grid_size, origin, x, y):
        self.grid_size = grid_size
        self.origin = origin
        self.x = x
        self.y = y

    @property
    def real_pos(self):
        return self.origin[0] + self.grid_size*self.x, \
               self.origin[1] + self.grid_size*self.y

    @property
    def pos(self):
        return self.x, self.y

    def update(self, rect):
        self.x, self.y = self.rect_to_position(rect)

    def rect_to_position(self, rect):
        x = (rect.x - self.origin[0]) // self.grid_size + 1
        y = (rect.y - self.origin[1]) // self.grid_size + 1
        return int(x), int(y)

    def position_to_point(self):
        x = self.origin[0] + self.x*self.grid_size
        y = self.origin[1] + self.y*self.grid_size
        return x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)




