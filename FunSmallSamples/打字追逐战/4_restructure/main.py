from cocos.director import director

from game import GameScene
from settings import Settings


if __name__ == '__main__':
    director.init(width=Settings.WIDTH, height=Settings.HEIGHT)
    director.run(GameScene())
