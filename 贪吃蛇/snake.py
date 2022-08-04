from cocos.layer import ColorLayer


class Pos(object):
    def __init__(self, pos, next_):
        self.pos = pos
        self.next = next_

    @property
    def up_pos(self):
        return self.pos[0], self.pos[1] + 1

    @property
    def down_pos(self):
        return self.pos[0], self.pos[1] - 1

    @property
    def left_pos(self):
        return self.pos[0] - 1, self.pos[1]

    @property
    def right_pos(self):
        return self.pos[0] + 1, self.pos[1]

    def go_up(self):
        new_pos = Pos(self.up_pos, next_=None)
        self.next = new_pos
        return new_pos

    def go_down(self):
        new_pos = Pos(self.down_pos, next_=None)
        self.next = new_pos
        return new_pos

    def go_left(self):
        new_pos = Pos(self.left_pos, next_=None)
        self.next = new_pos
        return new_pos

    def go_right(self):
        new_pos = Pos(self.right_pos, next_=None)
        self.next = new_pos
        return new_pos


class GridBody(ColorLayer):
    def __init__(self, pos, config, color=(10, 10, 200, 255)):
        super().__init__(*color, config.GRID_SIZE - 1, config.GRID_SIZE - 1)

        self.position = (config.ORIGIN.x + pos.pos[0] * config.GRID_SIZE,
                         config.ORIGIN.y + pos.pos[1] * config.GRID_SIZE)


class SnakeBody(GridBody):
    def __init__(self, pos, config, color=(10, 10, 200, 255)):
        super().__init__(pos, config, color)


class SnakeHead(GridBody):
    def __init__(self, pos, config, color=(0, 0, 0, 255)):
        super().__init__(pos, config, color)


class AppleProp(GridBody):
    def __init__(self, pos, config, color=(250, 10, 10, 255)):
        super().__init__(pos, config, color)


class Snake(object):
    def __init__(self, game_layer):
        # 每个grid存body类的信息, 方便移除
        self.direction = "up"
        self.game_layer = game_layer
        self.head = Pos((0, 0), None)
        self.pre_head = None
        self.tail = self.head
        self.body_len = 1  # 长度计数, 是决定何时开始区分body和head的条件, 若用head.pos != tail.pos有风险, 他俩根据这段程序也有可能相等(追尾)
        self.is_grow = False  # 是否吃到apple
        self.create_body(self.head)

    def move(self):
        # 如果可以走
        if self.check_valid(eval(f"self.head.{self.direction}_pos")):
            pos = eval(f"self.head.{self.direction}_pos")
            # 如果是道具
            if isinstance(self.game_layer.grids[pos], AppleProp):
                self.body_len += 1  
                self.is_grow = True
                self.game_layer.remove(self.game_layer.grids[pos])
                self.game_layer.prop_spawn_places = {pos: 1 for pos in self.game_layer.grids if
                                                     self.game_layer.grids[pos] is None}
                # 无处安放apple代表snake占满, 游戏胜利
                if not self.game_layer.prop_spawn_places:
                    self.game_layer.succeed()
                else:
                    self.game_layer.spawn_prop()

            if self.body_len > 1:
                self.pre_head = self.head
            self.head = eval(f"self.head.go_{self.direction}()")
            if not self.is_grow:
                self.game_layer.remove(self.game_layer.grids[self.tail.pos])
                self.game_layer.grids[self.tail.pos] = None
                self.tail = self.tail.next
            self.create_body(self.head)
            self.is_grow = False
        else:
            self.game_layer.game_over()

    def create_body(self, pos: Pos):
        snake_head = SnakeHead(pos=pos,
                               config=self.game_layer.config)
        self.game_layer.add(snake_head, z=100)
        self.game_layer.grids[pos.pos] = snake_head

        if self.pre_head:
            if isinstance(self.game_layer.grids[self.pre_head.pos], SnakeHead):
                self.game_layer.remove(self.game_layer.grids[self.pre_head.pos])
                snake_body = SnakeBody(pos=self.pre_head,
                                       config=self.game_layer.config)
                self.game_layer.add(snake_body, z=100)
                self.game_layer.grids[self.pre_head.pos] = snake_body

    def check_valid(self, pos):
        # 碰到身体或撞墙游戏失败
        if pos[0] < 0 or pos[0] >= self.game_layer.config.columns or \
                pos[1] < 0 or pos[1] >= self.game_layer.config.rows:
            return False
        if isinstance(self.game_layer.grids[pos], SnakeBody) and not pos == self.tail.pos:
            return False
        return True
