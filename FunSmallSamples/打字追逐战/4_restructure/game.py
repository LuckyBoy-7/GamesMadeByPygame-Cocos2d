from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.layer import Layer
from cocos.text import Label
from pyglet.window import key

from settings import Settings
from grid import Player, Enemy, build_maze, Pos, Background


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()

        self.add(ColorLayer(127, 127, 155, 255), z=1)  # 背景涂白
        self.add(TypingLayer(), z=2)
        self.add(ChasingLayer(), z=2)


class TypingLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(TypingLayer, self).__init__()

        self.is_running = True  # 是否敲完

        self.spec_ch = {"COMMA": ",",
                        "SPACE": " ",
                        "APOSTROPHE": "'",
                        "_8": "*",
                        "_1": "!",
                        "SLASH": "?"}  # 特殊字符, 因为key模块又不区分大小写, 这些字符又很难搞

        self.text_init()  # 生成文字模板

    def create_label(self, txt, color=None) -> Label:
        if color is None:
            color = 255, 255, 255, 255

        label = Label(txt,
                      position=Settings.typing_start,
                      color=color,
                      anchor_x="left", anchor_y="center", font_size=30)
        self.add(label)

        return label

    @staticmethod
    def _get_txt() -> str:
        with open("2.txt", "r", encoding="utf-8") as f:
            return " ".join(f.read().split())

    def text_init(self) -> None:
        self.original_text = list(self._get_txt())
        self.typing_text = []
        self.mask = self.create_label("".join(self.original_text))
        self.cur = self.need_move_idx = 0  # 分别指向original_text和typing_text

    def _move(self) -> None:
        width = self.typing_text[-1].element.content_width
        x, y = self.mask.position
        self.mask.position = x - width, y
        for label_idx in range(self.need_move_idx, len(self.typing_text)):
            label = self.typing_text[label_idx]

            x, y = label.position
            label.position = x - width, y
            if x - width < 0:
                self.need_move_idx += 1  # 把当前字母舍弃[移动了也看不到]

    def create_new_letter(self) -> None:
        letter = self.original_text[self.cur]
        label = self.create_label(letter, color=(0, 0, 250, 255))
        self.typing_text.append(label)

        self.cur += 1
        if self.cur == len(self.original_text):
            self.is_running = False

    def _handle_typing(self, pressed) -> None:
        current_letter = self.original_text[self.cur].upper()
        pressed = key.symbol_string(pressed)
        print(pressed)
        if pressed == current_letter \
                or (pressed in self.spec_ch and self.spec_ch[pressed] == current_letter):
            self.create_new_letter()  # 生成新的字母
            self._move()  # 整体(带字母)向左移动

            self.chasing_layer.player.idx = (
                                                        self.chasing_layer.player.idx + self.chasing_layer.player.direct * 1) % len(
                ChasingLayer.route)

    def on_key_press(self, pressed, _) -> None:
        if self.is_running:
            self._handle_typing(pressed)

    def on_enter(self):
        super().on_enter()

        for z, child in self.parent.children:
            if isinstance(child, ChasingLayer):
                self.chasing_layer = child
                break


def elapsed(threshold=10):
    def wrapper(func):
        elapsed = 0

        def inner(self):
            nonlocal elapsed
            elapsed += 1
            if elapsed >= threshold:
                elapsed = 0
                func(self)

        return inner

    return wrapper


class ChasingLayer(Layer):
    is_event_handler = True

    matrix, route = build_maze()

    def __init__(self):
        super(ChasingLayer, self).__init__()

        self.character_init()
        self.grids_init()

        self.schedule(self.update)

    def character_init(self):
        self.player = Player(self.route)
        self.add(self.player)

        self.enemy = Enemy(self.route)
        self.add(self.enemy)

    def grids_init(self):
        for i in range(Settings.COLUMNS):
            for j in range(Settings.ROWS):
                if self.matrix[j][i] == 0:
                    self.set_grid(Pos(i, j))

    def update(self, dt):
        self._handle_enemy_move()

    @elapsed(threshold=20)
    def _handle_enemy_move(self):
        self.enemy.move(self.player)

    def set_grid(self, pos):
        self.add(Background(pos))
