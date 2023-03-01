import random

from cocos.layer import Layer
from pyglet.gl import *
from cocos.sprite import Sprite
from cocos.batch import BatchNode

from image import Image


class BackgroundLayer(Layer):
    SPEED_ROAD = 3
    SPEED_CLOUD = 1.5

    def __init__(self):
        super().__init__()

        self.background_x = 0
        self.judge = 0
        self.b1 = Sprite(Image.background, anchor=(0, 0), position=(0, 80))
        self.b2 = Sprite(Image.background, anchor=(0, 0), position=(0, 80))
        self.add(self.b1)
        self.add(self.b2)

        # 云层部分
        self.elapsed = 0
        self.clouds = []

    def update(self):
        self.move()
        self.update_clouds()

    def update_clouds(self):
        self.elapsed += 0.1
        # 控制生成速率
        if self.elapsed > 15:
            self.elapsed = 0
            temp = Sprite(Image.cloud, position=(random.randint(1400, 1600), random.randint(300, 600)))
            temp.scale = 2
            temp.opacity = 128
            self.clouds.append(temp)
            self.add(temp)
        for cloud in self.clouds:
            # 如果越界则清除
            if cloud.x + cloud.width / 2 < 0:
                self.clouds.remove(cloud)
                del cloud
                break
            # 移动
            cloud.x -= BackgroundLayer.SPEED_CLOUD

    # 背景无限延伸
    def move(self):
        if self.background_x + self.b1.width <= 0:
            if not self.judge:
                self.background_x = self.b2.x
            else:
                self.background_x = self.b1.x
            self.judge += 1
        self.background_x -= BackgroundLayer.SPEED_ROAD
        # 当judge==2的倍数时
        if not self.judge % 2:
            self.b1.x = self.background_x
            self.b2.x = self.background_x + self.b1.width
        else:
            self.b2.x = self.background_x
            self.b1.x = self.background_x + self.b1.width

    def update_score(self):
        pass
