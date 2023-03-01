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
        self.cur = self.need_move_idx = 0

    def text_init(self):
        self.original_text = list(self._get_txt())
        self.typing_text = []
        self.mask = Label("".join(self.original_text),
                          position=start,
                          anchor_x="left", anchor_y="center", font_size=30)
        self.add(self.mask)

    def on_key_press(self, pressed, modifier):
        if self.is_running:
            key.symbol_string(pressed)

            current_letter = self.original_text[self.cur].upper()
            pressed = key.symbol_string(pressed)
            print(pressed, current_letter)
            if pressed == current_letter \
                    or (pressed in self.spec_ch and self.spec_ch[pressed] == current_letter):
                self.create_new_letter()

    def create_new_letter(self):
        letter = self.original_text[self.cur]
        if not self.typing_text:
            pos = start
        else:
            last_letter = self.typing_text[-1]
            pos = last_letter.position[0] + last_letter.element.content_width, last_letter.position[1]

        label = Label(letter,
                      position=pos,
                      color=(100, 100, 100, 255),
                      anchor_x="left", anchor_y="center", font_size=30)
        self.add(label)
        self.typing_text.append(label)
        self._move(label.element.content_width)

        self.cur += 1
        if self.cur == len(self.original_text):
            self.is_running = False

    def _move(self, width):
        print(self.need_move_idx)
        for label_idx in range(self.need_move_idx, len(self.typing_text)):
            label = self.typing_text[label_idx]
            x, y = label.position
            label.position = x - width, y
            if x - width < 0:
                self.need_move_idx += 1
        x, y = self.mask.position
        self.mask.position = x - width, y

    @staticmethod
    def _get_txt():
        with open("1.txt", "r", encoding="utf-8") as f:
            return " ".join(f.read().split())


if __name__ == '__main__':
    director.init(width=1400, height=800)

    GRID_SIZE = 24
    ROWS = 31  # 都要是奇数
    COLUMNS = 31

    width, height = director.get_window_size()
    ORIGIN = width / 2 - COLUMNS / 2 * GRID_SIZE, height / 2 - ROWS / 2 * GRID_SIZE
    start = width / 2, height / 2

    director.run(TypeScene())
