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
from cocos.actions import Hide


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


class BinarySearchScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(ColorLayer(127, 127, 127, 155))
        self.add(BinarySearchLayer())


class BinarySearchLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.i = 1
        self.elapsed = 0
        self.auto = False

        self.draw_bars()
        self.route = []
        self.create_route()

        self.left, self.mid, self.right = self.route[0]
        self.backup_left = self.left
        self.backup_mid = self.mid
        self.backup_right = self.right

        self.create_arrow()
        self.create_hint()

        self.schedule(self.update)

    def update(self, dt):
        self.left.color = CURRENT_COLOR_LEFT[:3]
        self.mid.color = CURRENT_COLOR_MID[:3]
        self.right.color = CURRENT_COLOR_RIGHT[:3]

        if self.auto:
            self.elapsed += 1
        if self.elapsed > 5:  # 粗暴
            self.elapsed = 0

            self.backup_left = self.left
            self.backup_mid = self.mid
            self.backup_right = self.right
            self.left, self.mid, self.right = self.route[self.i]
            self.arrow_left.position = self.left.x + self.left.width / 2, self.left.y + self.left.height + 100
            self.arrow_mid.position = self.mid.x + self.mid.width / 2, self.mid.y - 100
            self.arrow_right.position = self.right.x + self.right.width / 2, self.right.y + self.right.height + 100

            self.backup_left.color = BAR_COLOR[:3]
            self.backup_mid.color = BAR_COLOR[:3]
            self.backup_right.color = BAR_COLOR[:3]

            self.i += 1
            if self.i == len(self.route):
                self.unschedule(self.update)
                self.left.color = CURRENT_COLOR_LEFT[:3]
                self.right.color = CURRENT_COLOR_RIGHT[:3]
                self.mid.color = CURRENT_COLOR_MID[:3]
                return

    def on_key_press(self, pressed, modifier):
        if pressed == key.SPACE:
            self.auto = not self.auto
        elif pressed == key.RETURN:
            self.elapsed += 100

    def draw_bars(self):
        for idx, bar in enumerate(orig_data, -1):
            bar.position = START[0] + BAR_WIDTH * idx, START[1]
            self.add(bar)

            bar.idx = idx  # 绑定idx方便arrow展示当前idx
            bar.draw_idx()
        orig_data[0].do(Hide())
        orig_data[-1].do(Hide())

    def create_route(self):
        left = 1
        right = len(orig_data) - 2
        while left <= right:
            mid = (left + right) // 2
            self.route.append((orig_data[left], orig_data[mid], orig_data[right]))
            if orig_data[mid] > target:
                right = mid - 1
            elif orig_data[mid] < target:
                left = mid + 1
            self.route.append((orig_data[left], orig_data[mid], orig_data[right]))

            if orig_data[mid] == target:
                break

    def create_arrow(self):
        l = self.left
        r = self.right
        m = self.mid
        self.arrow_left = Label("left",
                                position=(l.x + l.width / 2, l.y + l.height + 100),
                                color=(255, 0, 0, 255),
                                font_size=30,
                                anchor_x="center",
                                anchor_y="center")
        self.arrow_right = Label("right",
                                 position=(r.x + r.width / 2, r.y + r.height + 100),
                                 color=(255, 0, 0, 255),
                                 font_size=30,
                                 anchor_x="center",
                                 anchor_y="center")
        self.arrow_mid = Label("mid",
                               position=(m.x + m.width / 2, m.y - 100),
                               color=(255, 0, 0, 255),
                               font_size=30,
                               anchor_x="center",
                               anchor_y="center")
        self.add(self.arrow_left)
        self.add(self.arrow_right)
        self.add(self.arrow_mid, z=10)

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

    BAR_WIDTH, BAR_HEIGHT = 75, 75  # bar的宽高
    BAR_NUMS = 15  # 数据个数
    BAR_NUMS = 16  # 数据个数
    BAR_COLOR = 190, 188, 127, 255
    CURRENT_COLOR_LEFT = 255, 0, 0, 100
    CURRENT_COLOR_MID = 0, 255, 0, 100
    CURRENT_COLOR_RIGHT = 0, 0, 255, 100

    START = width / 2 - BAR_NUMS / 2 * BAR_WIDTH, height / 2 - BAR_HEIGHT / 2

    orig_data = sorted([Bar(randint(1, 100)) for i in range(BAR_NUMS + 2)], key=lambda x: x.num)
    data = orig_data[1:-1]
    # target = Bar(1000)
    # target = Bar(-100)
    # target = data[-1]
    # target = data[0]
    target = choice(data)

    director.run(BinarySearchScene())
