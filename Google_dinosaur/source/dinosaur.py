from cocos.director import director
from game import GameScene


# 定义程序入口
def run_game():
    director.init(width=1320, height=720)

    director.run(GameScene())


if __name__ == '__main__':
    run_game()

