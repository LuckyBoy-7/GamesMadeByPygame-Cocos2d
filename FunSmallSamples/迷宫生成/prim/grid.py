from cocos.layer import ColorLayer, Layer
from cocos.text import Label

from settings import Settings
from position import Pos


class Grid(ColorLayer):
    def __init__(
            self,
            pos: Pos,
            color: tuple,
            exec_time: int = 0
    ):
        super().__init__(*color, Settings.GRID_SIZE - 1, Settings.GRID_SIZE - 1)

        self.pos = pos
        self.exec_time = exec_time

        self.position = self.pos.pos_to_position()
        self.anchor = self.width / 2, self.height / 2
        # 处理显示次数相关事宜
        self._handle_show_time()

    def _adjust_label(self, label) -> None:
        while label.element.content_width > self.width or label.element.content_height > self.height:
            label.element.font_size -= 5

    def _create_show_time_label(self) -> None:
        label = Label(f"{self.exec_time}", font_size=30, anchor_x="center", anchor_y="center")
        label.x, label.y = self.width / 2, self.height / 2
        self.add(label)
        # 调整大小
        self._adjust_label(label)

    def _handle_show_time(self) -> None:
        if Settings.show_num:  # 如果要显示的话
            # 创建Label
            self._create_show_time_label()


class End(Grid):
    def __init__(self, pos, exec_time=0):
        super().__init__(pos=pos, color=(0, 255, 0, 255), exec_time=exec_time)


class Start(Grid):
    def __init__(self, pos, exec_time=0):
        super().__init__(pos=pos, color=(255, 0, 0, 255), exec_time=exec_time)


class Block(Grid):
    def __init__(self, pos, exec_time=0):
        super().__init__(pos=pos, color=(0, 0, 0, 255), exec_time=exec_time)




