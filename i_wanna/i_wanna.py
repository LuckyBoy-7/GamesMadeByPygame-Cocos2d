from cocos.director import director
from cocos.scene import Scene

from game import GameScene, GameLayer


def run_game():
    director.init(caption="Your's I wanna", width=800, height=640)

    main_scene = GameScene()

    director.run(main_scene)


if __name__ == '__main__':
    run_game()
