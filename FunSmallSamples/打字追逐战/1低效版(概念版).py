from random import *
from collections import deque

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label
from cocos.rect import Rect
from cocos.actions import FadeIn, Delay, Hide, Show
from pyglet.window import key


class TypeScene(Scene):
    def __init__(self):
        super(TypeScene, self).__init__()

        self.add(ColorLayer(127, 127, 155, 255), z=1)  # 背景涂白
        self.add(TypeLayer(), z=2)


class TypeLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(TypeLayer, self).__init__()

        self.is_running = True
        self.spec_ch = {"COMMA": ",",
                        "SPACE": " "}

        self.text_init()
        self.cur = 0

    def text_init(self):
        self.original_text = list(self._get_txt())
        self.typing_text = []
        for letter in self.original_text:
            if not self.typing_text:
                pos = start
            else:
                last_letter = self.typing_text[-1]
                pos = last_letter.position[0] + last_letter.element.content_width, last_letter.position[1]

            label = Label(letter,
                          position=pos,
                          anchor_x="left", anchor_y="center", font_size=30)
            self.add(label)
            self.typing_text.append(label)

    def on_key_press(self, pressed, modifier):
        if self.is_running:
            key.symbol_string(pressed)

            obj = self.typing_text[self.cur]
            current_letter = obj.element.text.upper()
            pressed = key.symbol_string(pressed)
            if pressed == current_letter \
                    or (pressed in self.spec_ch and self.spec_ch[pressed] == current_letter):
                obj.element.color = 100, 100, 100, 100
                self.update(obj.element.content_width)

    def update(self, width):
        self._move(width)
        self.cur += 1
        if self.cur == len(self.typing_text):
            self.is_running = False

    def _move(self, width):
        for label in self.typing_text:
            x, y = label.position
            label.position = x - width, y


    @staticmethod
    def _get_txt():
        with open("1.txt", "r", encoding="utf-8") as f:
            return " ".join(f.read().split()[:10])


if __name__ == '__main__':
    director.init(width=1400, height=800)

    GRID_SIZE = 24
    ROWS = 31  # 都要是奇数
    COLUMNS = 31

    width, height = director.get_window_size()
    ORIGIN = width / 2 - COLUMNS / 2 * GRID_SIZE, height / 2 - ROWS / 2 * GRID_SIZE
    start = width / 2, height / 2

    director.run(TypeScene())
