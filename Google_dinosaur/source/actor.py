from cocos.sprite import Sprite
from pyglet.window import key
from cocos.director import director
from cocos.collision_model import AARectShape
from cocos.euclid import Vector2

from image import Image


class Hero(Sprite):
    LEFT, RIGHT = range(2)
    Speed = 3
    Ground = 70  # 高度
    JumpSpeed = 160
    Gravity = 3
    DASH_SPEED = 250

    def __init__(self):
        super().__init__(Image.dinosaur_run_right[Hero.RIGHT],
                         anchor=(Image.dinosaur_run_right[0].width / 2, 0))  # anchor位于中下

        # 出生位置
        self.position_backup = 100, 70
        self.position = 100, 70
        self.direction = Hero.RIGHT
        self.image_idx = 0

        # 基本参数
        self.life = 15
        self.invincible = False

        # 决定跳跃状态
        self.may_jump = True
        self.on_ground = False
        self.elapsed = 0
        self.elapsed_animation = 0
        self.in_sky = False

        # 决定冲刺状态
        self.dash = True
        self.dash_elapsed = 0
        self.dash_lock = False

        # 碰撞
        self.cshape = AARectShape(Vector2(self.x, self.y), self.width / 2 - 10, self.height / 2 - 10)

    def _update(self):
        self.update_position()
        self.update_animation()
        self.update_cshape()

    # 更新移动
    def update_position(self):
        self.y -= Hero.Gravity if self.y > Hero.Ground else 0
        # 没一直按着UP并且已落地
        if not self.key[key.UP]:
            self.may_jump = self.on_ground = True if self.y <= Hero.Ground else False
        # 左右跳蹲
        if self.key[key.RIGHT]:
            if self.x + self.width / 2 <= director.get_window_size()[0]:
                self.x += Hero.Speed
        if self.key[key.LEFT]:
            if self.x - self.width / 2 >= 0:
                self.x -= Hero.Speed
        if self.key[key.UP] and self.may_jump or self.in_sky:
            self.handle_jump()
        if self.key[key.DOWN]:
            self.y -= 10 if self.y - 10 > Hero.Ground else 0

        # 冲刺
        self.dash_elapsed += 0.1
        if self.dash_elapsed >= 3:
            self.dash = True
            self.dash_elapsed = 0
        if not self.key[key.D] and self.is_on_ground():
            self.dash_lock = False
        if self.key[key.D]:
            self.handle_dash()

    # 更新动画
    def update_animation(self):
        self.elapsed_animation += 0.1
        if self.elapsed_animation >= 1:
            self.image_idx = not self.image_idx
            self.elapsed_animation = 0

        if self.key[key.RIGHT]:
            self.direction = Hero.RIGHT
        elif self.key[key.LEFT]:
            self.direction = Hero.LEFT

        if self.key[key.DOWN]:
            self.image = Image.dinosaur_squat[self.direction][self.image_idx]
        else:
            self.image = Image.dinosaur_run[self.direction][self.image_idx]

    # 精细化跳跃, 多帧进行, 自然流畅
    def handle_jump(self):
        self.in_sky = True
        self.elapsed += 0.1
        self.y += Hero.JumpSpeed / 12
        if self.elapsed >= 1.8:
            self.elapsed = 0
            self.may_jump = False
            self.in_sky = False

    def handle_dash(self):
        if self.dash and not self.dash_lock:
            self.dash_lock = True
            # 朝右
            if self.direction == Hero.RIGHT:
                if self.x + self.width / 2 + Hero.DASH_SPEED >= director.get_window_size()[0]:
                    delta = director.get_window_size()[0] - (self.x + self.width / 2) + 1
                    self.x += delta
                else:
                    self.x += Hero.DASH_SPEED
            else:
                if self.x - self.width / 2 - Hero.DASH_SPEED <= 0:
                    delta = self.x - self.width / 2 + 2
                    self.x -= delta
                else:
                    self.x -= Hero.DASH_SPEED

    def is_on_ground(self):
        return self.on_ground is True

    def on_enter(self):
        super().on_enter()
        # 获取键盘状态, 以控制dinosaur
        self.key = key.KeyStateHandler()
        director.window.push_handlers(self.key)

    def update_cshape(self):
        self.cshape = AARectShape(Vector2(self.x, self.y), self.width / 2 - 10, self.height / 2 - 10)

    def restart(self):
        self.life = 1
        self.invincible = False
        self.position = self.position_backup







