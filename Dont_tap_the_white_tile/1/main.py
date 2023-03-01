"""
本来想做一个任意大小的, 结果诸事不顺, 就先混过去吧
"""

from cocos.director import director

from settings import Settings
from game import GameScene


def main():
    director.init(width=Settings.WIDTH, height=Settings.HEIGHT)
    director.run(GameScene())


if __name__ == '__main__':
    main()
