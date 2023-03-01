from cocos.scene import Scene
from cocos.layer import Layer
from cocos.tiles import load
from cocos.collision_model import CollisionManagerGrid
from cocos.director import director
from pyglet.window import key
from cocos.draw import Line
from cocos.actions import *
from cocos.particle_systems import *
from cocos.sprite import Sprite

from image import Image
from actor import Hero, Spike



director.init()
class GameScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(GameLayer(), z=2)


class GameLayer(Layer):
    def __init__(self):
        super().__init__()

        self.hero = Sprite("stand.png")
        self.hero.position = (100, 100)
        self.add(self.hero)

        self.add(DeathEffect(self.hero.position))


class DeathEffect(Explosion):
    total_particles = 1000
    size = 100

    def __init__(self, pos):
        super().__init__()

        self.__class__.texture = Image.blood.get_texture()
        self.position = pos

director.run(GameScene())