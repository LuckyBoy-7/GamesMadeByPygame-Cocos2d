from cocos.director import director

from settings import Settings
from game import GameScene


def run_game():
    director.init(
        width=Settings.WIDTH,
        height=Settings.HEIGHT
    )

    director.run(GameScene())


if __name__ == '__main__':
    run_game()
