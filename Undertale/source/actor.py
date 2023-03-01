from cocos.sprite import Sprite
from pyglet.window import key
from cocos.director import director
from cocos.collision_model import CircleShape
from cocos.euclid import Vector2

from image import Image


class Heart(Sprite):
    Speed = 3

    def __init__(self):
        super().__init__(Image.heart)  # anchor位于中下

        # 出生位置
        w, h = director.get_window_size()
        self.position = self.position_backup = w / 2, h / 2

        # 基本参数
        # self.hp = 1
        self.hp = 88
        self.invincible = False

        # 碰撞
        self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2 - 5)

    def _update(self):
        self.update_position()
        self.update_cshape()

    # 更新移动
    def update_position(self):
        if not self.parent.level.mess_time:
            if self.key[key.RIGHT]:
                if self.x + self.width / 2 <= director.get_window_size()[0]:
                    self.x += Heart.Speed
            if self.key[key.LEFT]:
                if self.x - self.width / 2 >= 0:
                    self.x -= Heart.Speed
            if self.key[key.UP]:
                if self.y + self.height / 2 <= 450:
                    self.y += Heart.Speed
            if self.key[key.DOWN]:
                if self.y - self.height / 2 >= 100:
                    self.y -= Heart.Speed
        else:
            if self.key[key.RIGHT]:
                if self.x - self.width / 2 >= 0:
                    self.x -= Heart.Speed
            if self.key[key.LEFT]:
                if self.x + self.width / 2 <= director.get_window_size()[0]:
                    self.x += Heart.Speed
            if self.key[key.UP]:
                if self.y - self.height / 2 >= 100:
                    self.y -= Heart.Speed
            if self.key[key.DOWN]:
                if self.y + self.height / 2 <= 450:
                    self.y += Heart.Speed

    def on_enter(self):
        super().on_enter()
        # 获取键盘状态, 以控制dinosaur
        self.key = key.KeyStateHandler()
        director.window.push_handlers(self.key)

    def update_cshape(self):
        self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2 - 5)

    def restart(self):
        self.opacity = 255
        self.hp = 88
        self.invincible = False
        self.position = self.position_backup



