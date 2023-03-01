from random import randint

from cocos.sprite import Sprite
from cocos.director import director
from cocos.rect import Rect
from cocos.collision_model import AARectShape, CircleShape
from cocos.euclid import Vector2

from image import Image


class Bird(Sprite):
    SPEED = 10
    LEFT, RIGHT = range(2)

    def __init__(self, direction):
        if direction == "right":
            super(Bird, self).__init__(Image.bird_fly[1][0])
            self.position = (-50, randint(10, 500))
            # self.position = (50, randint(10, 500))  # test code
        else:
            super(Bird, self).__init__(Image.bird_fly[0][0])
            self.position = (director.get_window_size()[0] + 50, randint(-50, 500))

        self.direction = direction
        self.image_idx = 0
        self.elapsed = 0

        # 扩大虚拟屏幕的范围, 既可以intersect, 又不用担心生成问题
        w, h = director.get_window_size()
        self.rect = Rect(-100, 100, 200 + w, 200 + h)

        # 更新碰撞
        self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2 - 4)

        self.schedule(self.update_)

    def update_(self, dt):
        self.update_position()
        self.update_animation()
        self.update_cshape()

    def update_position(self):
        if self.direction == "right":
            self.x += 4
        elif self.direction == "left":
            self.x -= 4

        if not self.get_rect().intersect(self.rect):
            self.kill()
            del self.parent.birds[0]

    def update_animation(self):
        self.elapsed += 0.1
        if self.elapsed >= 6:
            self.image_idx = not self.image_idx
            if self.direction == "right":
                self.image = Image.bird_fly[1][self.image_idx]
            else:
                self.image = Image.bird_fly[0][self.image_idx]
            self.elapsed = 0

    def update_cshape(self):
        self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2 - 4)




