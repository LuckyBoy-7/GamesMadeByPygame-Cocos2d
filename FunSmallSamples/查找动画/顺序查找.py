"""
现在用yield来实现试试更新
"""

from random import randint, choice
from math import ceil

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label
from pyglet.window import key


class Bar(ColorLayer):
    def __init__(self, num):
        super().__init__(*BAR_COLOR, BAR_WIDTH, BAR_HEIGHT)

        self.num = num
        self.anchor = 0, self.height / 2

        self.draw_outlines()
        self.draw_num()

    def __eq__(self, other):
        return self.num == other.num

    def __gt__(self, other):
        return self.num > other.num

    def __ge__(self, other):
        return self.num >= other.num

    def __lt__(self, other):
        return self.num < other.num

    def __le__(self, other):
        return self.num <= other.num

    def draw_num(self):
        label = Label(f"{self.num}",
                      position=(self.width / 2, self.height / 2),
                      font_size=30,
                      anchor_x="center",
                      anchor_y="center")
        while label.element.content_width > BAR_WIDTH:  # 适配bar的宽高
            label.element.content_width -= 5
        self.add(label)

    def draw_outlines(self):
        self.add(Line(start=(0, 0),
                      end=(0, self.height),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)
        self.add(Line(start=(0, self.height),
                      end=(self.width, self.height),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)
        self.add(Line(start=(self.width, 0),
                      end=(self.width, self.height),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)
        self.add(Line(start=(0, 0),
                      end=(self.width, 0),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)

    def draw_idx(self):
        self.add(Label(f"{self.idx}",
                       position=(self.width / 2, self.height + 40),
                       color=(0, 255, 0, 155),
                       font_size=30,
                       anchor_x="center",
                       anchor_y="center"))


class SequentialSearchScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(ColorLayer(127, 127, 127, 155))
        self.add(SequentialSearchLayer())


class SequentialSearchLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.i = 0
        self.elapsed = 0
        self.auto = False

        self.draw_bars()
        self.route = []
        self.create_route()
        self.create_arrow()
        self.create_hint()

        # print(self.route)
        self.schedule(self.update)

    def update(self, dt):
        self.route[self.i].color = CURRENT_COLOR[:3]
        tmp = self.route[self.i]
        self.arrow.position = tmp.x + tmp.width / 2, tmp.y + tmp.height + 100

        if self.auto:
            self.elapsed += 1
        if self.elapsed > 5:  # 粗暴
            self.elapsed = 0

            self.backup = self.i
            self.i += 1
            if self.i == len(self.route):
                self.unschedule(self.update)
                return
            self.route[self.backup].color = BAR_COLOR[:3]

    def on_key_press(self, pressed, modifier):
        if pressed == key.SPACE:
            self.auto = not self.auto
        elif pressed == key.RETURN:
            self.elapsed += 100

    def draw_bars(self):
        for idx, bar in enumerate(data):
            bar.position = START[0] + BAR_WIDTH * idx, START[1]
            self.add(bar)

            bar.idx = idx  # 绑定idx方便arrow展示当前idx
            bar.draw_idx()

    def create_route(self):
        for num in data:
            self.route.append(num)
            if num == target:
                break

    def create_arrow(self):
        tmp = self.route[self.i]
        self.arrow = Label("cur",
                           position=(tmp.x + tmp.width / 2, tmp.y + tmp.height + 100),
                           color=(255, 0, 0, 255),
                           font_size=30,
                           anchor_x="center",
                           anchor_y="center")
        self.add(self.arrow)

    def create_hint(self):
        msg = "in" if target in data else "not in "
        self.add(Label(f"target: {target.num} [state: {msg} data]",
                       position=(0, height),
                       font_size=30,
                       anchor_x="left",
                       anchor_y="top"))


if __name__ == '__main__':
    """回车到下一个状态, 空格切换自动模式"""
    director.init(width=1400, height=800)
    width, height = director.get_window_size()

    BAR_WIDTH, BAR_HEIGHT = 100, 100  # bar的宽高
    BAR_NUMS = 13  # 数据个数
    BAR_COLOR = 190, 188, 127, 255
    CURRENT_COLOR = 255, 0, 0, 255

    START = width / 2 - BAR_NUMS / 2 * BAR_WIDTH, height / 2 - BAR_HEIGHT / 2

    data = [Bar(randint(1, 100)) for i in range(BAR_NUMS)]
    # target = Bar(1000)
    target = data[-1]
    # target = choice(data)

    director.run(SequentialSearchScene())
