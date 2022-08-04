"""
x * y的贪吃蛇网格游戏
"""
from cocos.director import director

from game import GameScene


def run_game():
    director.init(
        width=1000,
        height=800
    )
    director.run(GameScene())


if __name__ == '__main__':
    run_game()