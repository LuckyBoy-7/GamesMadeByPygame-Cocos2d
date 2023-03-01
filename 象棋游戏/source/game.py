from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.draw import Line
from cocos.director import director
from cocos.rect import Rect

from chess import *


class MyScene(Scene):
    def __init__(self, game_layer):
        super().__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=0)

        self.game_layer = game_layer
        self.add(game_layer, z=10)


class MyLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        # 绘制棋盘
        self.grid_size = 76  # 19 * 4
        self.draw_board(self.grid_size)  # grid_size
        self.grid_rects = []
        self.set_grid_rects()
        print(len(self.grid_rects))

        # 绘制棋子
        self.all_chess = []
        self.current_chess = None
        self.draw_chess()

        # 显示选择
        self.choice_dots = []
        self.choice_rects = []
        self.whether_to_show = True

        self.schedule(self.update)

    def update(self, dt):
        self.update_chosen_state()

    def update_chosen_state(self):
        for child in self.all_chess:
            if child.rect.contains(*self.mouse_pos):  # 鼠标悬停
                # print("collide")
                child.opacity = 180
                if self.is_mouse_press:
                    self.current_chess = child
                    self.show_choices(self.current_chess)
                    self.whether_to_show = True
                    child.opacity = 50
            else:
                child.opacity = 255
        self.is_mouse_press = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = x, y

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.is_mouse_press = True
        if buttons == 1:
            for rect in self.choice_rects:  # 遍历所有路径
                if rect.contains(x, y):  # 如果点到了可以走的
                    for ces in self.all_chess:  # 遍历所有棋子
                        if ces.rect.contains(x, y):  # 如果棋子被点到了
                            self.current_chess.move(rect, self.all_chess, "eat")
                            break
                    else:  # 没点到棋子
                        self.current_chess.move(rect, self.all_chess, "move")
                    self.whether_to_show = False

                    # 清除预选的rect
                    self.choice_rects.clear()
                    # 清除绘制的dot
                    for dot in self.choice_dots:
                        dot.kill()
                    self.choice_dots.clear()

    def on_enter(self):  # on_mouse_motion比update触发的晚, 所以先声明
        super().on_enter()
        self.mouse_pos = 0, 0
        self.is_mouse_press = False

    def draw_board(self, grid: int):
        self.origin = director.get_window_size()[0] / 2 - grid * 4.5, \
                      director.get_window_size()[1] / 2 - grid * 4.5
        self.end = (self.origin[0] + 8 * grid,
                    self.origin[1] + 9 * grid)
        # self.board_rect = Rect(*self.origin, 8 * grid, 9 * grid)

        # n个格子 -> n + 2条线
        for row in range(10):
            if row == 4 or row == 5:
                line = Line((self.origin[0], self.origin[1] + grid * row),  # x不变
                            (self.end[0], self.origin[1] + grid * row),
                            color=(255, 0, 0, 255))
            else:
                line = Line((self.origin[0], self.origin[1] + grid * row),  # x不变
                            (self.end[0], self.origin[1] + grid * row),
                            color=(0, 0, 0, 255))
            self.add(line, z=0)
        for col in range(9):
            line = Line((self.origin[0] + grid * col, self.origin[1]),  # y不变
                        (self.origin[0] + grid * col, self.end[1]),
                        color=(0, 0, 0, 255))
            self.add(line, z=0)

    def set_grid_rects(self):
        for row in range(10):
            for col in range(9):
                self.grid_rects.append(
                    Rect(self.origin[0] + self.grid_size * (col - 0.5),  # 返回中心
                         self.origin[1] + self.grid_size * (row - 0.5),
                         self.grid_size,
                         self.grid_size
                         )
                )

    def draw_chess(self):
        # draw pawns
        black_pawns_pos = [Point(self.grid_size, self.origin, 0, 3),
                           Point(self.grid_size, self.origin, 2, 3),
                           Point(self.grid_size, self.origin, 4, 3),
                           Point(self.grid_size, self.origin, 6, 3),
                           Point(self.grid_size, self.origin, 8, 3)]
        red_pawns_pos = [Point(self.grid_size, self.origin, 0, 6),
                         Point(self.grid_size, self.origin, 2, 6),
                         Point(self.grid_size, self.origin, 4, 6),
                         Point(self.grid_size, self.origin, 6, 6),
                         Point(self.grid_size, self.origin, 8, 6)]
        for black_pawn_pos, red_pawn_pos in zip(black_pawns_pos, red_pawns_pos):
            temp1 = Pawn(black_pawn_pos, "black")
            temp2 = Pawn(red_pawn_pos, "red")
            self.all_chess.append(temp1)
            self.all_chess.append(temp2)
            self.add(temp1)
            self.add(temp2)

        # draw cars
        black_cars_pos = [Point(self.grid_size, self.origin, 0, 0),
                          Point(self.grid_size, self.origin, 8, 0)]
        red_cars_pos = [Point(self.grid_size, self.origin, 0, 9),
                        Point(self.grid_size, self.origin, 8, 9)]
        for black_cars_pos, red_cars_pos in zip(black_cars_pos, red_cars_pos):
            temp1 = Car(black_cars_pos, "black")
            temp2 = Car(red_cars_pos, "red")
            self.all_chess.append(temp1)
            self.all_chess.append(temp2)
            self.add(temp1)
            self.add(temp2)

        # draw cannons
        black_cannon_pos = [Point(self.grid_size, self.origin, 1, 2),
                            Point(self.grid_size, self.origin, 7, 2)]
        red_cannon_pos = [Point(self.grid_size, self.origin, 1, 7),
                          Point(self.grid_size, self.origin, 7, 7)]
        for black_cannon_pos, red_cannon_pos in zip(black_cannon_pos, red_cannon_pos):
            temp1 = Cannon(black_cannon_pos, "black")
            temp2 = Cannon(red_cannon_pos, "red")
            self.all_chess.append(temp1)
            self.all_chess.append(temp2)
            self.add(temp1)
            self.add(temp2)

        # draw horses
        black_horse_pos = [Point(self.grid_size, self.origin, 1, 0),
                           Point(self.grid_size, self.origin, 7, 0)]
        red_horse_pos = [Point(self.grid_size, self.origin, 1, 9),
                         Point(self.grid_size, self.origin, 7, 9)]
        for black_horse_pos, red_horse_pos in zip(black_horse_pos, red_horse_pos):
            temp1 = Horse(black_horse_pos, "black")
            temp2 = Horse(red_horse_pos, "red")
            self.all_chess.append(temp1)
            self.all_chess.append(temp2)
            self.add(temp1)
            self.add(temp2)

        # draw elephants
        black_elephant_pos = [Point(self.grid_size, self.origin, 2, 0),
                              Point(self.grid_size, self.origin, 6, 0)]
        red_elephant_pos = [Point(self.grid_size, self.origin, 2, 9),
                            Point(self.grid_size, self.origin, 6, 9)]
        for black_elephant_pos, red_elephant_pos in zip(black_elephant_pos, red_elephant_pos):
            temp1 = Elephant(black_elephant_pos, "black")
            temp2 = Elephant(red_elephant_pos, "red")
            self.all_chess.append(temp1)
            self.all_chess.append(temp2)
            self.add(temp1)
            self.add(temp2)

        # draw guards
        black_guard_pos = [Point(self.grid_size, self.origin, 3, 0),
                           Point(self.grid_size, self.origin, 5, 0)]
        red_guard_pos = [Point(self.grid_size, self.origin, 3, 9),
                         Point(self.grid_size, self.origin, 5, 9)]
        for black_guard_pos, red_guard_pos in zip(black_guard_pos, red_guard_pos):
            temp1 = Guard(black_guard_pos, "black")
            temp2 = Guard(red_guard_pos, "red")
            self.all_chess.append(temp1)
            self.all_chess.append(temp2)
            self.add(temp1)
            self.add(temp2)

        # draw kings
        temp1 = King(Point(self.grid_size, self.origin, 4, 0), "black")
        temp2 = King(Point(self.grid_size, self.origin, 4, 9), "red")
        self.all_chess.append(temp1)
        self.all_chess.append(temp2)
        self.add(temp1)
        self.add(temp2)

    def show_choices(self, chess):
        if self.whether_to_show:
            # 清除上次预选的rect
            self.choice_rects.clear()

            # 清除上次绘制的dot
            for dot in self.choice_dots:
                dot.kill()
            self.choice_dots.clear()

            # 绘制的可能路线
            for pos in chess.try_move(self.all_chess):
                for ces in self.all_chess:
                    # 如果路线和棋子重合(友军略去, 敌军改变hint颜色)
                    if ces.rect.contains(*pos.real_pos):
                        if chess.camp != ces.camp:  # 敌军
                            temp = Line(pos.real_pos, (pos.real_pos[0], pos.real_pos[1] + 1),
                                        (255, 0, 0, 100), stroke_width=20)
                            self.choice_dots.append(temp)
                            self.add(temp)

                            # 加载预选的rect(红色可吃)
                            for rect in self.grid_rects:
                                if rect.contains(*pos.real_pos):
                                    self.choice_rects.append(rect)
                            break

                else:  # 没碰撞, 则走普通路线
                    temp = Line(pos.real_pos, (pos.real_pos[0], pos.real_pos[1] + 1),
                                (0, 255, 0, 100), stroke_width=20)
                    self.choice_dots.append(temp)
                    self.add(temp)
                    # 加载预选的rect(绿色普通路线)
                    for rect in self.grid_rects:
                        if rect.contains(*pos.real_pos):
                            self.choice_rects.append(rect)
