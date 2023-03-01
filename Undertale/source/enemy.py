from random import randint, choice

from cocos.sprite import Sprite
from cocos.director import director
from cocos.rect import Rect
from cocos.collision_model import AARectShape, CircleShape
from cocos.euclid import Vector2

from image import Image
from math import sin


class Actor(Sprite):
    def __init__(self, img, up, down, name=None):
        super().__init__(img)

        self.name = name
        self.up, self.down = up, down
        w, h = director.get_window_size()
        self.rect = Rect(-100, 100, 200 + w, 200 + h)

        # 确定碰撞类型
        if name == "Bubble":
            self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2 - 4)
        else:
            self.cshape = AARectShape(Vector2(self.x, self.y), self.width / 2, self.height / 2)

        self.schedule(self.update_)

    def update_(self, dt):
        self.update_cshape()
        self.update_position()

    def update_position(self):
        pass

    def update_cshape(self):
        if self.name == "Bubble":
            self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2 - 4)
        else:
            self.cshape = AARectShape(Vector2(self.x, self.y), self.width / 2, self.height / 2)


class Bubble(Actor):
    SPEED = 1

    def __init__(self, up, down):
        super().__init__(Image.bubble, up, down, "Bubble")

        self.direction = [choice([-3, -2, -1, 1, 2]),
                          choice([-2, -1, 1, 2, 3])]
        self.position = (randint(0, director.get_window_size()[0] - self.width / 2),
                         randint(down + self.height / 2, up - self.height / 2))

    def update_position(self):
        self.edge_protect()
        self.x += self.direction[0] * Bubble.SPEED
        self.y += self.direction[1] * Bubble.SPEED

    def edge_protect(self):
        if self.x + self.width / 2 > director.get_window_size()[0] \
                or self.x - self.width / 2 < 0:
            self.direction[0] = -self.direction[0]
        if self.y + self.height / 2 > self.up \
                or self.y - self.height / 2 < self.down:
            self.direction[1] = -self.direction[1]


class Bone(Actor):
    SPEED = 2
    SPEED1 = 8
    GAP1 = 45
    GAP2 = 300
    GAP3 = 30

    def __init__(self, up, down, height, frequency, is_down, level):
        super().__init__(Image.bone, up, down, "Bone")

        self.direction = [-1, 1]
        self.scale = 3
        self.level = level
        w = director.get_window_size()[0]
        # sin_bone
        if self.level == 1:
            if is_down:
                self.position = w + frequency*Bone.GAP1, sin(height)*50 - 40
            else:
                self.position = w + frequency*Bone.GAP1, sin(height)*50 + 480
            self.change_direction_in_level1 = False
        # up_down_bone
        elif self.level == 2:
            self.change_direction_elapsed = 0
            self.change_direction = 1
            if is_down:
                self.position = w + frequency*Bone.GAP2, sin(height)*50 - 50
            else:
                self.position = w + frequency*Bone.GAP2, sin(height)*50 + 500
        elif self.level == 3:
            self.change_direction_elapsed = 0
            self.change_direction = 1
            if is_down:
                self.position = 0 + frequency*Bone.GAP3, -60
            else:
                self.position = 0 + frequency*Bone.GAP3, 470

    def update_position(self):
        if self.level == 1:
            # print(self.x)
            if self.x < -120 or self.change_direction_in_level1:
                self.x += self.direction[1] * Bone.SPEED1
                self.change_direction_in_level1 = True
            else:
                self.x += self.direction[0] * Bone.SPEED1
        elif self.level == 2:
            self.x += self.direction[0] * Bone.SPEED
            self.y += self.change_direction * Bone.SPEED

            self.change_direction_elapsed += 1
            if self.change_direction_elapsed > 100:
                self.change_direction = -self.change_direction
                self.change_direction_elapsed = 0
        elif self.level == 3:
            self.y += self.change_direction * Bone.SPEED

            self.change_direction_elapsed += 1
            if self.change_direction_elapsed > 100:
                self.change_direction = -self.change_direction
                self.change_direction_elapsed = 0
