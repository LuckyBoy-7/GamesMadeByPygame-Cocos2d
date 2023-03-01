from cocos.scene import Scene
from cocos.layer import Layer
from cocos.tiles import load
from cocos.collision_model import CollisionManagerGrid
from cocos.director import director
from pyglet.window import key
from cocos.draw import Line
from cocos.actions import *
from cocos.particle_systems import *
from pyglet.shapes import Rectangle

from image import Image
from actor import Hero, Spike
from trap import Trap


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        game_map = load("i_wanna_map.tmx")
        background_layer = game_map["background"]
        obstacle_layer = game_map["obstacle"]
        objects_layer = game_map["objects"]
        tileset = game_map["tileset"]

        background_layer.set_view(0, 0, 800, 640)
        obstacle_layer.set_view(0, 0, 800, 640)

        self.add(background_layer, z=0)
        self.add(obstacle_layer, z=1)
        self.add(GameLayer(obstacle_layer, objects_layer), z=2)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self, maplayer, objects_layer):
        super().__init__()

        self.maplayer = maplayer
        self.objects_layer = objects_layer

        self.hero = Hero(self.objects_layer.match(label="start")[0].position, self.maplayer)
        self.add(self.hero)

        self.spikes = {}

        # 绘制刺
        for spike in self.objects_layer.match(label="spike"):
            # print(index)
            if spike["orientation"] == "up":
                cell = maplayer.get_at_pixel(*spike.position)
                pos = cell.x + cell.width / 2, cell.y + cell.height / 2
                self.spikes[spike["index"]] = Spike(0, pos)
                self.add(self.spikes[spike["index"]])
            elif spike["orientation"] == "down":
                cell = maplayer.get_at_pixel(*spike.position)
                pos = cell.x + cell.width / 2, cell.y + cell.height / 2
                self.spikes[spike["index"]] = Spike(180, pos)
                self.add(self.spikes[spike["index"]])
            elif spike["orientation"] == "right":
                cell = maplayer.get_at_pixel(*spike.position)
                pos = cell.x + cell.width / 2, cell.y + cell.height / 2
                self.spikes[spike["index"]] = Spike(90, pos)
                self.add(self.spikes[spike["index"]])
            elif spike["orientation"] == "left":
                cell = maplayer.get_at_pixel(*spike.position)
                pos = cell.x + cell.width / 2, cell.y + cell.height / 2
                self.spikes[spike["index"]] = Spike(270, pos)
                self.add(self.spikes[spike["index"]])

        # 陷阱
        self.trap = Trap(objects_layer, self.maplayer)

        width, height = director.get_window_size()
        self.cm = CollisionManagerGrid(0, width, 0, height, 40, 40)

        self.schedule(self.update)

        self.time = True

    def update(self, dt):
        self.hero.update_(dt)
        self.update_collide()
        self.update_rect_collide()
        self.trap.update(self.hero.get_rect())
        self.trap.touch(self.spikes)

    def update_rect_collide(self):
        if self.time == True:
            # 下
            self.line1 = Line((self.hero.cshape.center[0] - self.hero.width / 2,
                               self.hero.cshape.center[1] - self.hero.height / 2),
                              (self.hero.cshape.center[0] + self.hero.width / 2,
                               self.hero.cshape.center[1] - self.hero.height / 2),
                              color=(255, 0, 0, 255))
            self.add(self.line1, z=10)

            # 左
            self.line2 = Line((self.hero.cshape.center[0] - self.hero.width / 2,
                               self.hero.cshape.center[1] - self.hero.height / 2),
                              (self.hero.cshape.center[0] - self.hero.width / 2,
                               self.hero.cshape.center[1] + self.hero.height / 2),
                              color=(255, 0, 0, 255))
            self.add(self.line2, z=10)

            # 右
            self.line3 = Line((self.hero.cshape.center[0] + self.hero.width / 2,
                               self.hero.cshape.center[1] - self.hero.height / 2),
                              (self.hero.cshape.center[0] + self.hero.width / 2,
                               self.hero.cshape.center[1] + self.hero.height / 2),
                              color=(255, 0, 0, 255))
            self.add(self.line3, z=10)

            # 上
            self.line4 = Line((self.hero.cshape.center[0] - self.hero.width / 2,
                               self.hero.cshape.center[1] + self.hero.height / 2),
                              (self.hero.cshape.center[0] + self.hero.width / 2,
                               self.hero.cshape.center[1] + self.hero.height / 2),
                              color=(255, 0, 0, 255))
            self.add(self.line4, z=10)
            self.time = False
        else:
            self.line1.start, self.line1.end = ((self.hero.cshape.center[0] - self.hero.width / 2,
                                                 self.hero.cshape.center[1] - self.hero.height / 2),
                                                (self.hero.cshape.center[0] + self.hero.width / 2,
                                                 self.hero.cshape.center[1] - self.hero.height / 2))

            self.line2.start, self.line2.end = ((self.hero.cshape.center[0] - self.hero.width / 2,
                                                 self.hero.cshape.center[1] - self.hero.height / 2),
                                                (self.hero.cshape.center[0] - self.hero.width / 2,
                                                 self.hero.cshape.center[1] + self.hero.height / 2))

            self.line3.start, self.line3.end = ((self.hero.cshape.center[0] + self.hero.width / 2,
                                                 self.hero.cshape.center[1] - self.hero.height / 2),
                                                (self.hero.cshape.center[0] + self.hero.width / 2,
                                                 self.hero.cshape.center[1] + self.hero.height / 2))

            self.line4.start, self.line4.end = ((self.hero.cshape.center[0] - self.hero.width / 2,
                                                 self.hero.cshape.center[1] + self.hero.height / 2),
                                                (self.hero.cshape.center[0] + self.hero.width / 2,
                                                 self.hero.cshape.center[1] + self.hero.height / 2))

    def update_collide(self):
        if self.hero.alive:
            self.cm.clear()

            for spike in self.spikes.values():
                self.cm.add(spike)
            self.cm.add(self.hero)

            for collided in self.cm.objs_colliding(self.hero):
                # print(collided)
                # self.cm.remove_tricky(self.hero)
                # self.remove(self.hero)
                self.hero.do(Hide())
                self.hero.alive = False
                self.hero.die_sound.play()
                self.add(DeathEffect(self.hero.position))
                return

    # reset()
    def on_key_press(self, pressed, _):
        # print(key)
        if pressed == key.R:
            self.reset()

    def reset(self):
        self.reset_hero()
        self.reset_trip()

    def reset_trip(self):
        pass

    def reset_hero(self):
        # self.hero.position = self.objects_layer.match(label="start")[0].position
        self.hero.alive = True
        self.hero.do(Show())


class DeathEffect(Explosion):
    size = 200
    total_particles = 100

    def __init__(self, pos):
        super().__init__()

        self.__class__.texture = Image.blood.get_texture()
        self.position = pos[0] + 90, pos[1] - 70

