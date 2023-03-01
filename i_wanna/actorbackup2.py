from random import randint

from cocos.sprite import Sprite
from cocos.collision_model import AARectShape, CircleShape
from cocos.euclid import Vector2
from cocos.mapcolliders import RectMapCollider
from pyglet.window import key
from cocos.director import director
from pyglet.media import load

from image import Image


class Hero(Sprite, RectMapCollider):
    LEFT, RIGHT = range(2)

    MOVE_SPEED = 120
    JUMP_SPEED = 360
    GRAVITY = -1000

    def __init__(self, pos, maplayer):
        Sprite.__init__(self, Image.stand[Hero.RIGHT])
        RectMapCollider.__init__(self, "slide")

        self.maplayer = maplayer

        self.position = pos

        self.cshape = AARectShape(Vector2(self.x, self.y), self.width, self.height)

        self.elapsed = 0
        self.velocity = 0, 0

        self.may_jump = True
        self.on_ground = True
        self.double_lst = []

        self.direction = Hero.RIGHT
        self.image_index = 0

        self.alive = True

        self.die_sound = load("die.wav", streaming=False)
        self.jump_sound = load("jump.wav", streaming=False)

        self.jump_time = 0
        self.lock = False

    def update_(self, dt):
        self.update_position(dt)
        self.update_animation(dt)
        self.update_cshape()

    def update_cshape(self):
        self.cshape.ry = self.height / 2
        self.cshape.rx = self.width / 2
        self.cshape = AARectShape(Vector2(self.x, self.y), self.width, self.height)

    def update_position(self, dt):
        if dt > 0.1:
            return

        view_x = self.maplayer.view_x
        view_w = self.maplayer.view_w

        vx, vy = self.velocity
        vx = (self.key[key.RIGHT] - self.key[key.LEFT]) * self.MOVE_SPEED
        vy += self.GRAVITY * dt

        # 实现二段跳
        self.double_lst.append(self.key[key.LSHIFT])
        if self.key[key.LSHIFT] and self.may_jump:
            vy, self.jump_time = self.handle_jump(vy, self.jump_time)
            vy += self.GRAVITY * 0.0001
            # print(self.double_lst)
            if len(self.double_lst) == 1:
                vy = self.JUMP_SPEED
                self.jump_sound.play()
            elif 0 in self.double_lst \
                    and 1 in self.double_lst[str(self.double_lst).find("0"):]:
                vy = 330
                self.may_jump = False
                self.jump_sound.play()

        if not self.key[key.LSHIFT] and self.on_ground:
            self.may_jump = True
            self.double_lst = []
        if self.on_ground:
            self.lock = False

        dx = vx * dt
        dy = vy * dt

        old = self.get_rect()
        new = old.copy()

        new.x += dx
        new.y += dy

        self.velocity = self.collide_map(self.maplayer, old, new, vx, vy)
        self.position = new.center

        self.on_ground = (new.bottom == old.bottom)
        # print(self.velocity)

    def update_animation(self, dt):
        if self.key[key.RIGHT]:
            self.direction = Hero.RIGHT
        if self.key[key.LEFT]:
            self.direction = Hero.LEFT

        old_height = self.get_rect().height

        if self.key[key.LSHIFT] and not self.on_ground:
            # 图片anchor变化, 待修复
            pass
            # self.image_index = not self.image_index
            # self.image = Image.jump[self.direction][self.image_index]
        elif (self.key[key.RIGHT] or self.key[key.LEFT]) and self.on_ground:
            self.elapsed += dt
            if self.elapsed > 0.06:
                self.image_index += 1
                if self.image_index > 3:
                    self.image_index = 0

                self.image = Image.run[self.direction][self.image_index]
                self.elapsed = 0
        else:
            self.image = Image.stand[self.direction]

        new_height = self.get_rect().height
        if new_height != old_height:
            self.image_anchor_y = new_height / 2
            self.y += new_height / 2

    def on_enter(self):
        super().on_enter()

        self.key = key.KeyStateHandler()
        director.window.push_handlers(self.key)

    def handle_jump(self, vy, time):
        if time > 3.8 or self.lock:
            self.lock = True
            return vy, 0

        if time == 0:
            vy = 350
        else:
            vy = 200
        time += 0.1
        return vy, time

class Spike(Sprite):
    def __init__(self, rotation, pos):
        super().__init__("spike.png", rotation=rotation, position=pos)

        self.cshape = CircleShape(Vector2(self.x, self.y), 1)

        self.schedule(self.update_cshape)

    def update_cshape(self, dt):
        self.cshape = CircleShape(Vector2(self.x, self.y), 1)
